# SHL Assessment Recommendation Engine - Solution Approach

## Problem Statement
Create a system that recommends appropriate SHL assessments based on job requirements and descriptions, with filtering capabilities and relevance-based ranking.

## Solution Architecture

### 1. Backend (FastAPI)
- **API Layer**: RESTful endpoints for recommendation requests
- **Processing Layer**: 
  - Text analysis using Google Gemini
  - Filtering by duration and test types
  - Cosine similarity for relevance ranking
- **Data Layer**: JSON-based assessment catalog

### 2. Frontend (Streamlit)
- Clean, intuitive interface
- Input fields for:
  - Job description/requirements
  - Maximum duration
  - Test type filters
- Real-time recommendations display

### 3. Key Components
- **Natural Language Processing**: Gemini API for understanding job requirements
- **Filtering System**: Duration and test type constraints
- **Ranking Algorithm**: Cosine similarity between query and assessment descriptions
- **API Integration**: FastAPI backend with Streamlit frontend

## Technical Implementation
1. **Data Processing**:
   - Load assessment catalog from JSON
   - Generate embeddings for text analysis
   - Calculate similarity scores

2. **API Endpoints**:
   - POST /recommend: Main recommendation endpoint
   - GET /docs: API documentation

3. **Frontend Features**:
   - Form-based input
   - Real-time filtering
   - Card-based results display

## Results
- Successfully implemented recommendation system
- Achieved real-time processing
- Maintained clean separation of concerns
- Provided intuitive user interface

## Future Improvements
- Enhanced error handling
- Caching for performance
- Additional filtering options
- User feedback integration 