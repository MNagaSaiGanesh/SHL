import streamlit as st
import requests
import pandas as pd
from typing import List, Optional

# Configure page
st.set_page_config(
    page_title="SHL Assessment Recommender",
    page_icon="🎯",
    layout="wide"
)

# Constants
API_URL = "http://localhost:8000"
TEST_TYPES = ["Cognitive", "Personality", "Behavioral", "Technical", "Skills"]

def get_recommendations(
    query_text: str,
    max_duration: Optional[int] = None,
    test_types: Optional[List[str]] = None
) -> List[dict]:
    """Get recommendations from the API"""
    try:
        response = requests.post(
            f"{API_URL}/recommend",
            json={
                "text": query_text,
                "max_duration": max_duration,
                "test_types": test_types
            }
        )
        response.raise_for_status()
        return response.json()["recommendations"]
    except Exception as e:
        st.error(f"Error getting recommendations: {str(e)}")
        return []

def main():
    # Header
    st.title("🎯 SHL Assessment Recommendation Engine")
    st.markdown("""
    Find the perfect SHL assessments for your hiring needs. Enter a job description,
    requirements, or any text describing what you're looking for.
    """)
    
    # Input section
    with st.form("recommendation_form"):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            query = st.text_area(
                "Enter your requirements or job description",
                height=150,
                placeholder="Example: Looking for Java developers who can collaborate effectively with business teams..."
            )
        
        with col2:
            max_duration = st.number_input(
                "Maximum assessment duration (minutes)",
                min_value=0,
                max_value=180,
                value=60,
                step=15
            )
            
            selected_types = st.multiselect(
                "Filter by test types",
                options=TEST_TYPES,
                default=[]
            )
        
        submitted = st.form_submit_button("Get Recommendations")
    
    # Get and display recommendations
    if submitted and query:
        with st.spinner("Finding the best assessments for you..."):
            recommendations = get_recommendations(
                query,
                max_duration if max_duration > 0 else None,
                selected_types if selected_types else None
            )
        
        if recommendations:
            st.subheader("📋 Recommended Assessments")
            
            # Convert to DataFrame for better display
            df = pd.DataFrame(recommendations)
            
            # Display each recommendation as a card
            for _, row in df.iterrows():
                with st.container():
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.markdown(f"### [{row['name']}]({row['url']})")
                        st.markdown(f"**Test Type:** {row['test_type']}")
                        st.markdown(f"**Duration:** {row['duration']}")
                    
                    with col2:
                        st.markdown("**Features:**")
                        st.markdown(f"- Remote Testing: {row['remote_testing']}")
                        st.markdown(f"- Adaptive/IRT: {row['adaptive_irt']}")
                    
                    st.markdown("---")
        else:
            st.warning("No assessments found matching your criteria. Try adjusting your filters.")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    ### About
    This recommendation engine uses advanced natural language processing to match your requirements
    with SHL's comprehensive assessment catalog. The recommendations are ranked based on relevance
    to your needs and filtered according to your specifications.
    """)

if __name__ == "__main__":
    main() 