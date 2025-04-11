from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
import json
import os
from typing import List, Optional
from dotenv import load_dotenv
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-pro')

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    text: str
    max_duration: Optional[int] = None
    test_types: Optional[List[str]] = None

class Assessment(BaseModel):
    name: str
    url: str
    remote_testing: str
    adaptive_irt: str
    duration: str
    test_type: str

def load_catalog():
    """Load the SHL catalog data"""
    try:
        with open("../data/shl_catalog.json", "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading catalog: {str(e)}")
        return []

def get_embedding(text: str):
    """Get embedding for text using Gemini"""
    response = model.generate_content(
        f"Analyze this text and provide key skills and requirements: {text}"
    )
    return response.text

def filter_assessments(assessments: List[dict], max_duration: Optional[int] = None, 
                      test_types: Optional[List[str]] = None) -> List[dict]:
    """Filter assessments based on duration and test types"""
    filtered = assessments.copy()
    
    if max_duration:
        filtered = [
            a for a in filtered 
            if "minute" in a["duration"].lower() and 
            int(''.join(filter(str.isdigit, a["duration"]))) <= max_duration
        ]
    
    if test_types:
        filtered = [
            a for a in filtered 
            if any(t.lower() in a["test_type"].lower() for t in test_types)
        ]
    
    return filtered

def rank_assessments(query: str, assessments: List[dict]) -> List[dict]:
    """Rank assessments based on relevance to query"""
    try:
        # Get query embedding
        query_embedding = get_embedding(query)
        
        # Get embeddings for each assessment
        assessment_embeddings = [
            get_embedding(f"{a['name']} {a['test_type']} {a['duration']}")
            for a in assessments
        ]
        
        # Calculate similarities
        similarities = [
            cosine_similarity(
                [query_embedding], 
                [assessment_emb]
            )[0][0]
            for assessment_emb in assessment_embeddings
        ]
        
        # Sort assessments by similarity
        ranked_assessments = [
            x for _, x in sorted(
                zip(similarities, assessments), 
                key=lambda pair: pair[0], 
                reverse=True
            )
        ]
        
        return ranked_assessments[:10]  # Return top 10
    except Exception as e:
        print(f"Error in ranking: {str(e)}")
        return assessments[:10]

@app.get("/")
def read_root():
    return {"message": "SHL Assessment Recommendation API"}

@app.post("/recommend")
def get_recommendations(query: Query):
    """Get assessment recommendations based on query"""
    try:
        # Load catalog
        catalog = load_catalog()
        if not catalog:
            raise HTTPException(status_code=500, detail="Failed to load catalog data")
        
        # Filter assessments
        filtered_assessments = filter_assessments(
            catalog,
            max_duration=query.max_duration,
            test_types=query.test_types
        )
        
        if not filtered_assessments:
            return {"recommendations": [], "message": "No assessments match your criteria"}
        
        # Rank assessments
        ranked_assessments = rank_assessments(query.text, filtered_assessments)
        
        return {
            "recommendations": ranked_assessments,
            "message": "Success"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/metrics")
def get_metrics():
    """Calculate and return evaluation metrics"""
    # This would be implemented with your test queries and known relevant results
    return {"mean_recall_at_3": 0.0, "map_at_3": 0.0}  # Placeholder 