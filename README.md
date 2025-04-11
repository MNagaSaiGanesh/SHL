# SHL Assessment Recommendation Engine

A web application that recommends SHL assessments based on job requirements and descriptions.

## Features

- Natural language processing for understanding job requirements
- Filtering by test duration and types
- Ranking assessments based on relevance
- Modern web interface with Streamlit
- RESTful API for integration

## Tech Stack

- Backend: FastAPI, Python
- Frontend: Streamlit
- AI: Google Gemini
- Data Processing: Pandas, NumPy

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd shl-assessment-recommender
```

2. Create and activate virtual environment:
```bash
python -m venv venv
# Windows
.\venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file:
```bash
cp .env.example .env
```
Then edit `.env` and add your Google API key:
```
GOOGLE_API_KEY=your_api_key_here
```

5. Start the backend server:
```bash
uvicorn backend.main:app --reload
```

6. Start the frontend (in a new terminal):
```bash
streamlit run frontend/app.py
```

## API Usage

The API is available at `http://localhost:8000`

### Endpoints

- `POST /recommend`: Get assessment recommendations
  ```json
  {
      "text": "your query text",
      "max_duration": 60,
      "test_types": ["Technical"]
  }
  ```

- `GET /docs`: Interactive API documentation

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License 