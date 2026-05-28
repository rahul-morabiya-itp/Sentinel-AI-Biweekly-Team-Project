# SentinelAI Gateway

## Setup Instructions

### 1. Create Virtual Environment

python -m venv venv

### 2. Activate Virtual Environment

venv\Scripts\activate

### 3. Install Requirements

pip install -r requirements.txt

### 4. Add Gemini API Key

Edit .env file.

### 5. Initialize Database

python init_db.py

### 6. Start FastAPI Server

uvicorn app.main:app --reload

### 7. Start Streamlit Dashboard

streamlit run app/dashboard/streamlit_app.py

---

## API Endpoint

POST http://127.0.0.1:8000/chat

### Example Request

{
    "source": "internal-copilot",
    "prompt": "Summarize the Q4 sales report"
}
