# Combined Project Codebase

This file contains the complete source code of the project.


---

# FILE: .env

```
GEMINI_API_KEY=A
DATABASE_URL=sqlite:///./data/logs.db

```


---

# FILE: .gitignore

```
# =========================
# Python
# =========================
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
dist/
downloads/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual Environments
venv/
env/
ENV/
.venv/

# =========================
# Streamlit
# =========================
.streamlit/secrets.toml

# Streamlit cache
.streamlit/cache/

# =========================
# Environment Variables
# =========================
.env
.env.*
!.env.example

# =========================
# Logs
# =========================
*.log
logs/

# =========================
# VS Code
# =========================
.vscode/

# =========================
# Jupyter Notebook
# =========================
.ipynb_checkpoints/

# =========================
# Testing / Coverage
# =========================
.pytest_cache/
.coverage
htmlcov/
.tox/
.mypy_cache/

# =========================
# OS Files
# =========================
.DS_Store
Thumbs.db

# =========================
# Database / Local Storage
# =========================
*.sqlite3
*.db

# =========================
# Temporary Files
# =========================
tmp/
temp/
*.tmp
```


---

# FILE: init_db.py

```python
from app.core.database import engine
from app.models.database_models import Base

Base.metadata.create_all(bind=engine)

print("Database initialized successfully.")

```


---

# FILE: migrateCode.py

```python
import os
from pathlib import Path

# =========================
# CONFIGURATION
# =========================

# Root folder of your application
ROOT_FOLDER = r"C:\proj\sentinel-ai-gateway"

# Output markdown file
OUTPUT_FILE = "combined_project_code.md"

# File extensions to include
INCLUDE_EXTENSIONS = {
    ".py",
    ".txt",
    ".md",
    ".json",
    ".yaml",
    ".yml",
    ".toml",
    ".ini",
    ".cfg",
    ".html",
    ".css",
    ".js",
    ".ts",
    ".tsx",
    ".jsx",
    ".sql",
    ".sh",
    ".bat",
    ".env",
}

# Folders to ignore
IGNORE_FOLDERS = {
    "__pycache__",
    ".git",
    ".idea",
    ".vscode",
    "node_modules",
    "venv",
    ".venv",
    "env",
    "dist",
    "build",
    ".pytest_cache",
    ".mypy_cache",
}

# Files to ignore
IGNORE_FILES = {
    OUTPUT_FILE,
}

# Map extensions to markdown code block languages
LANGUAGE_MAP = {
    ".py": "python",
    ".js": "javascript",
    ".ts": "typescript",
    ".tsx": "tsx",
    ".jsx": "jsx",
    ".html": "html",
    ".css": "css",
    ".json": "json",
    ".yaml": "yaml",
    ".yml": "yaml",
    ".md": "markdown",
    ".sql": "sql",
    ".sh": "bash",
    ".bat": "bat",
    ".toml": "toml",
    ".ini": "ini",
}


# =========================
# HELPERS
# =========================

def should_include_file(file_path: Path):
    if file_path.name in IGNORE_FILES:
        return False

    if file_path.suffix.lower() in INCLUDE_EXTENSIONS:
        return True

    special_names = {
        "Dockerfile",
        ".gitignore",
        ".env",
    }

    if file_path.name in special_names:
        return True

    return False


def get_language(file_path: Path):
    if file_path.name == "Dockerfile":
        return "dockerfile"

    return LANGUAGE_MAP.get(file_path.suffix.lower(), "")


# =========================
# MAIN FUNCTION
# =========================

def combine_project_to_markdown(root_folder, output_file):
    root_path = Path(root_folder)

    with open(output_file, "w", encoding="utf-8") as outfile:

        # Optional project title
        outfile.write("# Combined Project Codebase\n\n")
        outfile.write(
            "This file contains the complete source code of the project.\n\n"
        )

        for current_root, dirs, files in os.walk(root_path):

            # Remove ignored folders
            dirs[:] = [d for d in dirs if d not in IGNORE_FOLDERS]

            for file_name in files:

                file_path = Path(current_root) / file_name

                if not should_include_file(file_path):
                    continue

                relative_path = file_path.relative_to(root_path)

                try:
                    with open(file_path, "r", encoding="utf-8") as infile:
                        content = infile.read()

                except UnicodeDecodeError:
                    try:
                        with open(file_path, "r", encoding="latin-1") as infile:
                            content = infile.read()
                    except Exception as e:
                        print(f"Skipping unreadable file: {relative_path}")
                        print(f"Reason: {e}")
                        continue

                except Exception as e:
                    print(f"Skipping file: {relative_path}")
                    print(f"Reason: {e}")
                    continue

                language = get_language(file_path)

                # Write file header
                outfile.write("\n")
                outfile.write("---\n\n")
                outfile.write(f"# FILE: {relative_path}\n\n")

                # Write fenced code block
                outfile.write(f"```{language}\n")
                outfile.write(content)
                outfile.write("\n```\n\n")

                print(f"Added: {relative_path}")

    print(f"\nDone! Markdown file created: {output_file}")


# =========================
# RUN
# =========================

if __name__ == "__main__":
    combine_project_to_markdown(ROOT_FOLDER, OUTPUT_FILE)
```


---

# FILE: migrateDB.py

```python
import sqlite3

conn = sqlite3.connect("data/logs.db")
cursor = conn.cursor()

# Get existing columns
cursor.execute("PRAGMA table_info(request_logs)")
columns = [col[1] for col in cursor.fetchall()]

if "provider" not in columns:
    cursor.execute(
        "ALTER TABLE request_logs ADD COLUMN provider TEXT"
    )

if "model_name" not in columns:
    cursor.execute(
        "ALTER TABLE request_logs ADD COLUMN model_name TEXT"
    )

conn.commit()
conn.close()
```


---

# FILE: README.md

```markdown
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

```


---

# FILE: requirements.txt

```
fastapi==0.115.0
uvicorn[standard]==0.30.6
streamlit==1.38.0
google-generativeai==0.7.2
python-dotenv==1.0.1
sqlalchemy==2.0.35
pandas==2.2.2
plotly==5.24.1
sentence-transformers==3.1.1
faiss-cpu==1.8.0.post1
scikit-learn==1.5.2
numpy==1.26.4
pydantic==2.9.2
httpx==0.27.2
streamlit-autorefresh

```


---

# FILE: app\main.py

```python
from fastapi import FastAPI

from app.api.routes import router


app = FastAPI(
    title="SentinelAI Gateway",
    version="1.0.0"
)


app.include_router(router)


@app.get("/")
def health():

    return {
        "status": "running",
        "service": "SentinelAI Gateway"
    }

```


---

# FILE: app\__init__.py

```python

```


---

# FILE: app\analyzers\advanced_risk_engine.py

```python
from dataclasses import dataclass
from typing import List


@dataclass
class RiskAnalysisResult:
    risk_level: str
    detected_categories: List[str]
    recommendations: List[str]


class AdvancedRiskEngine:

    HIGH_RISK_KEYWORDS = {
        "password": "Credential Exposure",
        "secret": "Sensitive Information",
        "salary": "HR Sensitive Data",
        "confidential": "Confidential Business Data",
        "private": "Privacy Risk",
        "token": "Credential Leakage",
        "ssn": "Personal Identity Risk",
        "credit card": "Financial Data Exposure"
    }

    def analyze(self, prompt: str) -> RiskAnalysisResult:

        detected_categories = []

        recommendations = []

        risk_score = 0

        lower_prompt = prompt.lower()

        for keyword, category in self.HIGH_RISK_KEYWORDS.items():

            if keyword in lower_prompt:
                detected_categories.append(category)
                risk_score += 25

        if risk_score >= 50:
            risk_level = "HIGH"
            recommendations.append(
                "Mask sensitive information before sending to external LLM"
            )

        elif risk_score >= 25:
            risk_level = "MEDIUM"
            recommendations.append(
                "Review prompt for sensitive content"
            )

        else:
            risk_level = "LOW"
            recommendations.append(
                "No major risks detected"
            )

        return RiskAnalysisResult(
            risk_level=risk_level,
            detected_categories=detected_categories,
            recommendations=recommendations
        )

```


---

# FILE: app\analyzers\ai_finops_engine.py

```python
from dataclasses import dataclass
from typing import Dict


@dataclass
class FinOpsInsight:
    estimated_monthly_cost: float
    optimization_potential: float
    waste_score: int
    recommendations: list


class AIFinOpsEngine:

    def generate_insights(
        self,
        total_tokens: int,
        duplicate_percentage: float,
        verbose_prompt_percentage: float
    ) -> FinOpsInsight:

        estimated_monthly_cost = round(
            total_tokens * 0.000001 * 30,
            2
        )

        optimization_potential = round(
            estimated_monthly_cost * (
                duplicate_percentage + verbose_prompt_percentage
            ) / 100,
            2
        )

        waste_score = min(
            int(
                duplicate_percentage + verbose_prompt_percentage
            ),
            100
        )

        recommendations = []

        if duplicate_percentage > 20:
            recommendations.append(
                "Enable semantic cache reuse"
            )

        if verbose_prompt_percentage > 30:
            recommendations.append(
                "Introduce prompt compression pipeline"
            )

        if waste_score > 50:
            recommendations.append(
                "Consider smaller models for low complexity tasks"
            )

        return FinOpsInsight(
            estimated_monthly_cost=estimated_monthly_cost,
            optimization_potential=optimization_potential,
            waste_score=waste_score,
            recommendations=recommendations
        )
```


---

# FILE: app\analyzers\intent_classifier.py

```python
def classify_intent(prompt: str):

    text = prompt.lower()

    if "summarize" in text:
        return "SUMMARIZATION"

    if "code" in text:
        return "CODING"

    if "analyze" in text:
        return "ANALYSIS"

    if "translate" in text:
        return "TRANSLATION"

    return "GENERAL"

```


---

# FILE: app\analyzers\optimization_recommendation_engine.py

```python
class OptimizationRecommendationEngine:

    def generate(
        self,
        duplicate_detected: bool,
        prompt_score: int,
        total_tokens: int,
        risk_level: str
    ):

        recommendations = []

        if duplicate_detected:
            recommendations.append(
                "Enable semantic cache reuse"
            )

        if prompt_score < 60:
            recommendations.append(
                "Improve prompt structure and clarity"
            )

        if total_tokens > 1000:
            recommendations.append(
                "Reduce unnecessary context size"
            )

        if risk_level == "HIGH":
            recommendations.append(
                "Route through secure internal model"
            )

        if not recommendations:
            recommendations.append(
                "No major optimization issues detected"
            )

        return recommendations
```


---

# FILE: app\analyzers\optimizer.py

```python
def generate_optimizations(prompt: str):

    suggestions = []

    word_count = len(prompt.split())

    if word_count > 120:
        suggestions.append(
            "Prompt is too verbose. Reduce unnecessary context."
        )

    if "explain everything" in prompt.lower():
        suggestions.append(
            "Specify concise output requirements."
        )

    if len(suggestions) == 0:
        suggestions.append(
            "Prompt appears reasonably optimized."
        )

    return suggestions

```


---

# FILE: app\analyzers\organizational_intelligence.py

```python
from collections import defaultdict


class OrganizationalIntelligence:

    def __init__(self):

        self.team_metrics = defaultdict(list)

    def record(
        self,
        source: str,
        latency: float,
        tokens: int,
        risk_level: str
    ):

        self.team_metrics[source].append({
            "latency": latency,
            "tokens": tokens,
            "risk": risk_level
        })

    def generate_summary(self):

        insights = {}

        for source, records in self.team_metrics.items():

            total_tokens = sum(r["tokens"] for r in records)

            avg_latency = round(
                sum(r["latency"] for r in records) / len(records),
                2
            )

            high_risk_count = len([
                r for r in records
                if r["risk"] == "HIGH"
            ])

            insights[source] = {
                "total_requests": len(records),
                "total_tokens": total_tokens,
                "average_latency": avg_latency,
                "high_risk_requests": high_risk_count
            }

        return insights

```


---

# FILE: app\analyzers\pii_scanner.py

```python
import re


EMAIL_PATTERN = r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'

PHONE_PATTERN = r'\b\d{10}\b'


def scan_pii(text: str):

    findings = []

    if re.search(EMAIL_PATTERN, text):
        findings.append("EMAIL")

    if re.search(PHONE_PATTERN, text):
        findings.append("PHONE")

    return findings

```


---

# FILE: app\analyzers\prompt_quality_analyzer.py

```python
from dataclasses import dataclass
from typing import List


@dataclass
class PromptQualityResult:
    score: int
    issues: List[str]
    recommendations: List[str]


class PromptQualityAnalyzer:

    def analyze(self, prompt: str) -> PromptQualityResult:

        issues = []
        recommendations = []

        score = 100

        word_count = len(prompt.split())

        if word_count > 150:
            score -= 20
            issues.append("Prompt excessively verbose")
            recommendations.append(
                "Reduce unnecessary context and verbosity"
            )

        if "explain everything" in prompt.lower():
            score -= 15
            issues.append("Ambiguous broad instruction")
            recommendations.append(
                "Specify exact output expectations"
            )

        if "please" not in prompt.lower() and len(prompt) < 20:
            score -= 10
            issues.append("Insufficient contextual clarity")
            recommendations.append(
                "Provide additional business context"
            )

        if "json" not in prompt.lower() and "format" not in prompt.lower():
            score -= 10
            recommendations.append(
                "Specify output format for consistency"
            )

        if score >= 85:
            recommendations.append(
                "Prompt structure appears strong"
            )

        score = max(score, 0)

        return PromptQualityResult(
            score=score,
            issues=issues,
            recommendations=recommendations
        )

```


---

# FILE: app\analyzers\risk_engine.py

```python
RISK_KEYWORDS = [
    "salary",
    "password",
    "secret",
    "confidential",
    "private",
    "api key"
]


def assess_risk(prompt: str):

    lower_prompt = prompt.lower()

    for keyword in RISK_KEYWORDS:

        if keyword in lower_prompt:
            return "HIGH"

    return "LOW"

```


---

# FILE: app\analyzers\semantic_detector.py

```python
from sentence_transformers import (
    SentenceTransformer
)

from sklearn.metrics.pairwise import (
    cosine_similarity
)

import numpy as np


# =========================================================
# EMBEDDING MODEL
# =========================================================

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

# =========================================================
# IN-MEMORY VECTOR STORE
# =========================================================

stored_prompts = []

stored_embeddings = []

SIMILARITY_THRESHOLD = 0.75

# =========================================================
# SEMANTIC SIMILARITY CHECK
# =========================================================

def check_similarity(prompt: str):

    global stored_prompts
    global stored_embeddings

    # =====================================================
    # EMPTY PROMPT SAFETY
    # =====================================================

    if not prompt.strip():

        return None

    # =====================================================
    # CREATE EMBEDDING
    # =====================================================

    embedding = model.encode(
        [prompt]
    )[0]

    # =====================================================
    # FIRST REQUEST
    # =====================================================

    if len(stored_embeddings) == 0:

        stored_prompts.append(
            prompt
        )

        stored_embeddings.append(
            embedding
        )

        return None

    # =====================================================
    # CALCULATE COSINE SIMILARITY
    # =====================================================

    similarities = cosine_similarity(
        [embedding],
        stored_embeddings
    )[0]

    max_score = float(
        np.max(similarities)
    )

    best_match_index = int(
        np.argmax(similarities)
    )

    # =====================================================
    # MATCH FOUND
    # =====================================================

    if max_score >= SIMILARITY_THRESHOLD:

        similar_prompt = (
            stored_prompts[
                best_match_index
            ]
        )

        # Store current prompt too
        stored_prompts.append(
            prompt
        )

        stored_embeddings.append(
            embedding
        )

        return {

            "similar_prompt": (
                similar_prompt
            ),

            "score": round(
                max_score,
                4
            )
        }

    # =====================================================
    # STORE NEW PROMPT
    # =====================================================

    stored_prompts.append(
        prompt
    )

    stored_embeddings.append(
        embedding
    )

    return None

# =========================================================
# DEBUG / METRICS
# =========================================================

def get_similarity_stats():

    return {

        "stored_prompts": len(
            stored_prompts
        ),

        "stored_embeddings": len(
            stored_embeddings
        ),

        "similarity_threshold": (
            SIMILARITY_THRESHOLD
        )
    }
```


---

# FILE: app\analyzers\workflow_intelligence.py

```python
from collections import defaultdict


class WorkflowIntelligenceEngine:

    def __init__(self):

        self.workflow_patterns = defaultdict(list)

    def track_workflow(
        self,
        source: str,
        intent: str
    ):

        self.workflow_patterns[source].append(intent)

    def generate_insights(self):

        insights = {}

        for source, intents in self.workflow_patterns.items():

            insights[source] = {
                "total_requests": len(intents),
                "top_workload": max(
                    set(intents),
                    key=intents.count
                )
            }

        return insights

```


---

# FILE: app\analyzers\__init__.py

```python

```


---

# FILE: app\api\routes.py

```python
import time
import traceback

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.models.request_models import ChatRequest
from app.models.database_models import RequestLog

from app.services.provider_manager import (
    provider_manager
)

from app.services.model_selector import (
    model_selector
)

from app.services.cost_calculator import (
    CostCalculator
)

from app.services.realtime_metrics import (
    metrics_store
)

from app.analyzers.intent_classifier import (
    classify_intent
)

from app.analyzers.pii_scanner import (
    scan_pii
)

from app.analyzers.semantic_detector import (
    check_similarity,
    get_similarity_stats
)

from app.analyzers.prompt_quality_analyzer import (
    PromptQualityAnalyzer
)

from app.analyzers.advanced_risk_engine import (
    AdvancedRiskEngine
)

from app.analyzers.optimization_recommendation_engine import (
    OptimizationRecommendationEngine
)

# =========================================================
# ROUTER
# =========================================================

router = APIRouter()

# =========================================================
# INITIALIZE ANALYZERS
# =========================================================

prompt_analyzer = PromptQualityAnalyzer()

risk_engine = AdvancedRiskEngine()

optimization_engine = (
    OptimizationRecommendationEngine()
)

# =========================================================
# HEALTH CHECK
# =========================================================

@router.get("/health")
def health_check():

    return {
        "status": "healthy",
        "service": "SentinelAI Gateway"
    }

# =========================================================
# REALTIME METRICS
# =========================================================

@router.get("/realtime-metrics")
def realtime_metrics():

    return metrics_store.get_metrics()

# =========================================================
# SEMANTIC SIMILARITY STATS
# =========================================================

@router.get("/similarity-stats")
def similarity_stats():

    return get_similarity_stats()

# =========================================================
# MAIN CHAT ENDPOINT
# =========================================================

@router.post("/chat")
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db)
):

    start_time = time.time()

    try:

        # =================================================
        # TRACK REQUEST
        # =================================================

        metrics_store.increment_requests()

        # =================================================
        # ANALYZE PROMPT
        # =================================================

        pii_findings = scan_pii(
            request.prompt
        )

        intent = classify_intent(
            request.prompt
        )

        prompt_quality = (
            prompt_analyzer.analyze(
                request.prompt
            )
        )

        risk_analysis = (
            risk_engine.analyze(
                request.prompt
            )
        )

        similarity = check_similarity(
            request.prompt
        )

        # =================================================
        # HIGH RISK TRACKING
        # =================================================

        if (
            risk_analysis.risk_level
            == "HIGH"
        ):

            metrics_store.add_high_risk()

        # =================================================
        # MODEL SELECTION
        # =================================================

        model_decision = (
            model_selector.select_model(
                intent=intent,
                risk_level=(
                    risk_analysis.risk_level
                ),
                prompt_quality_score=(
                    prompt_quality.score
                )
            )
        )

        provider_name = (
            model_decision["provider"]
        )

        model_name = (
            model_decision["model"]
        )

        # =================================================
        # PROVIDER EXECUTION
        # =================================================

        llm_response = (
            provider_manager.generate(
                provider_name=provider_name,
                model_name=model_name,
                prompt=request.prompt
            )
        )

        # =================================================
        # LATENCY
        # =================================================

        latency = round(
            time.time() - start_time,
            2
        )

        # =================================================
        # REAL COST CALCULATION
        # =================================================

        real_cost = (
            CostCalculator.calculate(
                model_name=(
                    llm_response["model"]
                ),
                input_tokens=(
                    llm_response[
                        "input_tokens"
                    ]
                ),
                output_tokens=(
                    llm_response[
                        "output_tokens"
                    ]
                )
            )
        )

        # =================================================
        # UPDATE REALTIME METRICS
        # =================================================

        metrics_store.add_tokens(
            llm_response[
                "total_tokens"
            ]
        )

        metrics_store.add_cost(
            real_cost
        )

        # =================================================
        # OPTIMIZATION ENGINE
        # =================================================

        recommendations = (
            optimization_engine.generate(
                duplicate_detected=(
                    similarity is not None
                ),
                prompt_score=(
                    prompt_quality.score
                ),
                total_tokens=(
                    llm_response[
                        "total_tokens"
                    ]
                ),
                risk_level=(
                    risk_analysis.risk_level
                )
            )
        )

        # =================================================
        # SIMILARITY SCORE
        # =================================================

        similarity_score = None

        if similarity:

            similarity_score = (
                similarity.get(
                    "score"
                )
            )

        # =================================================
        # DATABASE LOGGING
        # =================================================

        log = RequestLog(

            source=request.source,

            provider=(
                llm_response[
                    "provider"
                ]
            ),

            model_name=(
                llm_response[
                    "model"
                ]
            ),

            prompt=request.prompt,

            response=(
                llm_response[
                    "response"
                ]
            ),

            intent=intent,

            risk_level=(
                risk_analysis.risk_level
            ),

            pii_detected=", ".join(
                pii_findings
            ),

            similarity_score=(
                similarity_score
            ),

            input_tokens=(
                llm_response[
                    "input_tokens"
                ]
            ),

            output_tokens=(
                llm_response[
                    "output_tokens"
                ]
            ),

            total_tokens=(
                llm_response[
                    "total_tokens"
                ]
            ),

            latency=latency,

            estimated_cost=real_cost,

            optimization=" | ".join(
                recommendations
            )
        )

        db.add(log)

        db.commit()

        db.refresh(log)

        # =================================================
        # RESPONSE PAYLOAD
        # =================================================

        return {

            "request_id": log.id,

            "provider": (
                llm_response[
                    "provider"
                ]
            ),

            "model": (
                llm_response[
                    "model"
                ]
            ),

            "response": (
                llm_response[
                    "response"
                ]
            ),

            "fallback_used": (
                llm_response.get(
                    "fallback_used",
                    False
                )
            ),

            "tried_models": (
                llm_response.get(
                    "tried_models",
                    []
                )
            ),

            "intent": intent,

            "risk_analysis": {

                "risk_level": (
                    risk_analysis.risk_level
                ),

                "categories": (
                    risk_analysis.detected_categories
                ),

                "recommendations": (
                    risk_analysis.recommendations
                )
            },

            "prompt_quality": {

                "score": (
                    prompt_quality.score
                ),

                "issues": (
                    prompt_quality.issues
                ),

                "recommendations": (
                    prompt_quality.recommendations
                )
            },

            "pii_findings": (
                pii_findings
            ),

            "similarity": (
                similarity
            ),

            "latency_seconds": (
                latency
            ),

            "token_usage": {

                "input_tokens": (
                    llm_response[
                        "input_tokens"
                    ]
                ),

                "output_tokens": (
                    llm_response[
                        "output_tokens"
                    ]
                ),

                "total_tokens": (
                    llm_response[
                        "total_tokens"
                    ]
                )
            },

            "cost_analysis": {

                "provider": (
                    llm_response[
                        "provider"
                    ]
                ),

                "model": (
                    llm_response[
                        "model"
                    ]
                ),

                "estimated_cost_usd": (
                    real_cost
                )
            },

            "optimization_recommendations": (
                recommendations
            )
        }

    # =====================================================
    # ERROR HANDLING
    # =====================================================

    except Exception as error:

        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail={
                "message": (
                    "AI Gateway processing failed"
                ),
                "error": str(error)
            }
        )
```


---

# FILE: app\api\__init__.py

```python

```


---

# FILE: app\cache\semantic_cache.py

```python
from typing import Dict


class SemanticCache:

    def __init__(self):

        self.cache = {}

    def get(self, similarity_key: str):

        return self.cache.get(similarity_key)

    def set(
        self,
        similarity_key: str,
        response: Dict
    ):

        self.cache[similarity_key] = response

```


---

# FILE: app\cache\__init__.py

```python

```


---

# FILE: app\core\config.py

```python
from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "sqlite:///./data/logs.db"
    )

settings = Settings()

```


---

# FILE: app\core\database.py

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

from app.core.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

```


---

# FILE: app\core\__init__.py

```python

```


---

# FILE: app\dashboard\advanced_dashboard_metrics.py

```python
import sqlite3
import pandas as pd


class DashboardMetrics:

    def load_data(self):

        connection = sqlite3.connect(
            "data/logs.db"
        )

        dataframe = pd.read_sql(
            "SELECT * FROM request_logs",
            connection
        )

        return dataframe

    def generate_summary(self, dataframe):

        return {
            "total_requests": len(dataframe),
            "total_tokens": dataframe[
                "total_tokens"
            ].sum(),
            "average_latency": round(
                dataframe["latency"].mean(),
                2
            ),
            "total_cost": round(
                dataframe["estimated_cost"].sum(),
                4
            )
        }

```


---

# FILE: app\dashboard\streamlit_app.py

```python
import sqlite3
from datetime import datetime

import pandas as pd
import requests
import streamlit as st
import plotly.express as px

from streamlit_autorefresh import st_autorefresh


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="SentinelAI Dashboard",
    page_icon="🛡️",
    layout="wide"
)

# =========================================================
# AUTO REFRESH
# =========================================================

REFRESH_INTERVAL_MS = 10000

st_autorefresh(
    interval=REFRESH_INTERVAL_MS,
    key="sentinel_dashboard_refresh"
)

# =========================================================
# CONSTANTS
# =========================================================

DATABASE_PATH = "data/logs.db"

API_BASE_URL = "http://127.0.0.1:8000"

# =========================================================
# PAGE HEADER
# =========================================================

st.title("🛡️ SentinelAI Gateway Dashboard")

st.markdown("""
### Enterprise AI Traffic Intelligence, Governance & AI FinOps Platform
""")

# =========================================================
# DATABASE HELPERS
# =========================================================

@st.cache_data(ttl=5)
def load_request_logs():

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    dataframe = pd.read_sql(
        "SELECT * FROM request_logs",
        connection
    )

    connection.close()

    return dataframe

# =========================================================
# REALTIME METRICS
# =========================================================

@st.cache_data(ttl=3)
def load_realtime_metrics():

    try:

        response = requests.get(
            f"{API_BASE_URL}/realtime-metrics",
            timeout=3
        )

        if response.status_code == 200:

            return response.json()

        return {}

    except Exception:

        return {}

# =========================================================
# SAFE HELPERS
# =========================================================

def safe_sum(dataframe, column_name):

    if column_name not in dataframe.columns:
        return 0

    return dataframe[column_name].fillna(0).sum()

def safe_mean(dataframe, column_name):

    if column_name not in dataframe.columns:
        return 0

    return round(
        dataframe[column_name].fillna(0).mean(),
        2
    )

# =========================================================
# MAIN APPLICATION
# =========================================================

try:

    dataframe = load_request_logs()

    realtime_metrics = load_realtime_metrics()

    # =====================================================
    # EMPTY STATE
    # =====================================================

    if dataframe.empty:

        st.warning(
            "No AI traffic logs available yet."
        )

        st.info(
            "Send requests through the gateway to begin monitoring."
        )

        st.stop()

    # =====================================================
    # SORT DATA
    # =====================================================

    if "id" in dataframe.columns:

        dataframe = dataframe.sort_values(
            by="id",
            ascending=False
        )

    # =====================================================
    # KPI CALCULATIONS
    # =====================================================

    total_requests = len(dataframe)

    total_tokens = safe_sum(
        dataframe,
        "total_tokens"
    )

    total_cost = safe_sum(
        dataframe,
        "estimated_cost"
    )

    average_latency = safe_mean(
        dataframe,
        "latency"
    )

    high_risk_requests = len(
        dataframe[
            dataframe["risk_level"] == "HIGH"
        ]
    )

    duplicate_requests = len(
        dataframe[
            dataframe["similarity_score"].notnull()
        ]
    )

    pii_requests = len(
        dataframe[
            dataframe["pii_detected"].fillna("") != ""
        ]
    )

    # =====================================================
    # LAST UPDATED
    # =====================================================

    last_updated = realtime_metrics.get(
        "last_updated",
        str(datetime.utcnow())
    )

    st.caption(
        f"Last Updated: {last_updated}"
    )

    # =====================================================
    # KPI SECTION
    # =====================================================

    st.subheader("Platform Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Requests",
        f"{total_requests:,}"
    )

    col2.metric(
        "Total Tokens",
        f"{int(total_tokens):,}"
    )

    col3.metric(
        "Total AI Spend",
        f"${total_cost:.6f}"
    )

    col4.metric(
        "Average Latency",
        f"{average_latency}s"
    )

    col5, col6, col7, col8 = st.columns(4)

    col5.metric(
        "High Risk Requests",
        high_risk_requests
    )

    col6.metric(
        "Duplicate Requests",
        duplicate_requests
    )

    col7.metric(
        "PII Requests",
        pii_requests
    )

    col8.metric(
        "Live AI Spend",
        f"${realtime_metrics.get('total_cost', total_cost):.6f}"
    )

    st.divider()

    # =====================================================
    # REALTIME TRAFFIC LOGS
    # =====================================================

    st.subheader("Realtime AI Traffic Logs")

    st.dataframe(
        dataframe,
        use_container_width=True,
        height=450
    )

    st.divider()

    # =====================================================
    # RISK & INTENT ANALYTICS
    # =====================================================

    col9, col10 = st.columns(2)

    with col9:

        st.subheader("Risk Distribution")

        if "risk_level" in dataframe.columns:

            fig_risk = px.pie(
                dataframe,
                names="risk_level",
                title="AI Risk Levels"
            )

            st.plotly_chart(
                fig_risk,
                use_container_width=True
            )

    with col10:

        st.subheader("Intent Distribution")

        if "intent" in dataframe.columns:

            fig_intent = px.histogram(
                dataframe,
                x="intent",
                title="Intent Classification"
            )

            st.plotly_chart(
                fig_intent,
                use_container_width=True
            )

    st.divider()

    # =====================================================
    # TOKEN & COST ANALYTICS
    # =====================================================

    col11, col12 = st.columns(2)

    with col11:

        st.subheader("Realtime Token Consumption")

        fig_tokens = px.line(
            dataframe,
            y="total_tokens",
            title="Token Usage Trends"
        )

        st.plotly_chart(
            fig_tokens,
            use_container_width=True
        )

    with col12:

        st.subheader("Realtime AI Spend")

        fig_cost = px.line(
            dataframe,
            y="estimated_cost",
            title="AI Cost Trends"
        )

        st.plotly_chart(
            fig_cost,
            use_container_width=True
        )

    st.divider()

    # =====================================================
    # MODEL USAGE INTELLIGENCE
    # =====================================================

    st.subheader("Model Usage Intelligence")

    if (
        "model_name" in dataframe.columns
        and
        "provider" in dataframe.columns
    ):

        model_metrics = dataframe.groupby(
            ["provider", "model_name"]
        ).agg({
            "total_tokens": "sum",
            "estimated_cost": "sum",
            "latency": "mean"
        }).reset_index()

        model_metrics["latency"] = (
            model_metrics["latency"]
            .round(2)
        )

        st.dataframe(
            model_metrics,
            use_container_width=True
        )

        fig_models = px.bar(
            model_metrics,
            x="model_name",
            y="estimated_cost",
            color="provider",
            title="Cost Per Model"
        )

        st.plotly_chart(
            fig_models,
            use_container_width=True
        )

    st.divider()

    # =====================================================
    # ORGANIZATIONAL ANALYTICS
    # =====================================================

    st.subheader(
        "Organizational AI Usage Intelligence"
    )

    if "source" in dataframe.columns:

        source_metrics = dataframe.groupby(
            "source"
        ).agg({
            "total_tokens": "sum",
            "estimated_cost": "sum",
            "latency": "mean"
        }).reset_index()

        source_metrics["latency"] = (
            source_metrics["latency"]
            .round(2)
        )

        st.dataframe(
            source_metrics,
            use_container_width=True
        )

        fig_source_cost = px.bar(
            source_metrics,
            x="source",
            y="estimated_cost",
            title="Cost Per Organizational Source"
        )

        st.plotly_chart(
            fig_source_cost,
            use_container_width=True
        )

    st.divider()

    # =====================================================
    # GOVERNANCE & SECURITY
    # =====================================================

    st.subheader(
        "AI Governance & Security Insights"
    )

    pii_dataframe = dataframe[
        dataframe["pii_detected"].fillna("") != ""
    ]

    if len(pii_dataframe) > 0:

        st.warning(
            "Sensitive information detected in prompts."
        )

        st.dataframe(
            pii_dataframe[[
                "source",
                "pii_detected",
                "risk_level",
                "prompt"
            ]],
            use_container_width=True
        )

    else:

        st.success(
            "No sensitive information detected."
        )

    st.divider()

    # =====================================================
    # SEMANTIC DUPLICATE DETECTION
    # =====================================================

    st.subheader(
        "Semantic Duplicate Detection"
    )

    duplicate_dataframe = dataframe[
        dataframe["similarity_score"].notnull()
    ]

    if len(duplicate_dataframe) > 0:

        st.info(
            "Potential reusable workloads detected."
        )

        st.dataframe(
            duplicate_dataframe[[
                "source",
                "prompt",
                "similarity_score"
            ]],
            use_container_width=True
        )

    else:

        st.success(
            "No semantic duplicates detected."
        )

    st.divider()

    # =====================================================
    # OPTIMIZATION INTELLIGENCE
    # =====================================================

    st.subheader(
        "Optimization Intelligence"
    )

    high_token_requests = dataframe[
        dataframe["total_tokens"] > 300
    ]

    if len(high_token_requests) > 0:

        st.warning(
            "High token usage workloads identified."
        )

        st.dataframe(
            high_token_requests[[
                "source",
                "model_name",
                "total_tokens",
                "estimated_cost",
                "optimization"
            ]],
            use_container_width=True
        )

    else:

        st.success(
            "No major optimization issues detected."
        )

    st.divider()

    # =====================================================
    # AI FINOPS INSIGHTS
    # =====================================================

    st.subheader("AI FinOps Insights")

    waste_score = min(
        int(
            (
                duplicate_requests /
                max(total_requests, 1)
            ) * 100
        ),
        100
    )

    potential_savings = round(
        total_cost * (
            waste_score / 100
        ),
        6
    )

    finops_col1, finops_col2 = st.columns(2)

    finops_col1.metric(
        "AI Waste Score",
        f"{waste_score}%"
    )

    finops_col2.metric(
        "Potential Savings",
        f"${potential_savings:.6f}"
    )

    st.markdown("""
### Optimization Recommendations

- Enable semantic caching
- Reuse duplicate AI workloads
- Route lightweight tasks to cheaper models
- Compress verbose prompts
- Standardize enterprise prompts
- Route sensitive requests to secure models
- Optimize high-cost organizational workloads
""")

    st.divider()

    # =====================================================
    # MODEL COST LEADERBOARD
    # =====================================================

    st.subheader("Model Cost Leaderboard")

    if "model_name" in dataframe.columns:

        leaderboard = dataframe.groupby(
            "model_name"
        ).agg({
            "estimated_cost": "sum",
            "total_tokens": "sum"
        }).reset_index()

        leaderboard = leaderboard.sort_values(
            by="estimated_cost",
            ascending=False
        )

        st.dataframe(
            leaderboard,
            use_container_width=True
        )

except Exception as error:

    st.error(
        f"Dashboard Error: {str(error)}"
    )
```


---

# FILE: app\dashboard\__init__.py

```python

```


---

# FILE: app\gateway\__init__.py

```python

```


---

# FILE: app\models\database_models.py

```python
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import Text

from app.core.database import Base


class RequestLog(Base):
    __tablename__ = "request_logs"

    id = Column(Integer, primary_key=True, index=True)

    source = Column(String, nullable=False)

    prompt = Column(Text, nullable=False)

    response = Column(Text, nullable=False)

    intent = Column(String)

    provider = Column(String)

    model_name = Column(String)

    risk_level = Column(String)

    pii_detected = Column(String)

    similarity_score = Column(Float)

    input_tokens = Column(Integer)

    output_tokens = Column(Integer)

    total_tokens = Column(Integer)

    latency = Column(Float)

    estimated_cost = Column(Float)

    optimization = Column(Text)

```


---

# FILE: app\models\request_models.py

```python
from pydantic import BaseModel


class ChatRequest(BaseModel):

    source: str

    prompt: str

```


---

# FILE: app\models\__init__.py

```python

```


---

# FILE: app\services\cost_calculator.py

```python
from app.services.model_registry import (
    MODEL_REGISTRY
)


class CostCalculator:

    @staticmethod
    def calculate(
        model_name: str,
        input_tokens: int,
        output_tokens: int
    ):

        pricing = MODEL_REGISTRY.get(
            model_name
        )

        if not pricing:

            return 0

        input_cost = (
            input_tokens / 1_000_000
        ) * pricing[
            "input_cost_per_million"
        ]

        output_cost = (
            output_tokens / 1_000_000
        ) * pricing[
            "output_cost_per_million"
        ]

        total_cost = (
            input_cost + output_cost
        )

        return round(
            total_cost,
            8
        )
```


---

# FILE: app\services\gemini_service.py

```python
import google.generativeai as genai

from app.core.config import settings


MODEL_NAME = "gemini-1.5-flash-8b"

genai.configure(
    api_key=settings.GEMINI_API_KEY
)

model = genai.GenerativeModel(
    model_name=MODEL_NAME
)


def ask_gemini(prompt: str):

    response = model.generate_content(prompt)

    response_text = response.text

    input_tokens = len(prompt.split())

    output_tokens = len(response_text.split())

    total_tokens = (
        input_tokens + output_tokens
    )

    return {
        "model": MODEL_NAME,
        "response": response_text,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": total_tokens
    }
```


---

# FILE: app\services\metrics_service.py

```python
def estimate_cost(total_tokens: int):

    return round(total_tokens * 0.000001, 6)

```


---

# FILE: app\services\model_registry.py

```python
MODEL_REGISTRY = {

    "gemini-1.5-flash-8b": {
        "provider": "google",
        "category": "fast",
        "supports_streaming": True,
        "input_cost_per_million": 0.0375,
        "output_cost_per_million": 0.15
    },

    "gemini-1.5-flash": {
        "provider": "google",
        "category": "balanced",
        "supports_streaming": True,
        "input_cost_per_million": 0.075,
        "output_cost_per_million": 0.30
    },

    # Current Google pricing
    "gemini-2.5-flash": {
        "provider": "google",
        "category": "advanced",
        "supports_streaming": True,
        "input_cost_per_million": 0.30,
        "output_cost_per_million": 2.50
    },

    "gemini-3.5-flash": {
        "provider": "google",
        "category": "advanced",
        "supports_streaming": True,
        "input_cost_per_million": 0.30,
        "output_cost_per_million": 2.50
    },

    "gemini-2.5-pro": {
        "provider": "google",
        "category": "premium",
        "supports_streaming": True,
        "input_cost_per_million": 1.25,
        "output_cost_per_million": 10.00
    },

    # GPT-4o pricing updated
    "openai-gpt4o": {
        "provider": "openai",
        "category": "premium",
        "supports_streaming": True,
        "input_cost_per_million": 2.50,
        "output_cost_per_million": 10.00
    },

    # Claude Sonnet pricing is correct
    "claude-sonnet": {
        "provider": "anthropic",
        "category": "balanced",
        "supports_streaming": True,
        "input_cost_per_million": 3.00,
        "output_cost_per_million": 15.00
    }
}
```


---

# FILE: app\services\model_selector.py

```python
class ModelSelector:

    def select_model(
        self,
        intent: str,
        risk_level: str,
        prompt_quality_score: int
    ):

        if risk_level == "HIGH":

            return {
                "provider": "google",
                "model": "gemini-1.5-flash"
            }

        if intent == "SUMMARIZATION":

            return {
                "provider": "google",
                "model": "gemini-1.5-flash-8b"
            }

        if intent == "CODING":

            return {
                "provider": "google",
                "model": "gemini-2.5-flash"
            }

        return {
            "provider": "google",
            "model": "gemini-1.5-flash"
        }


model_selector = ModelSelector()
```


---

# FILE: app\services\pricing_registry.py

```python
MODEL_PRICING = {

    "gemini-1.5-flash": {
        "provider": "google",
        "input_per_million": 0.075,
        "output_per_million": 0.30
    },

    "gemini-1.5-flash-8b": {
        "provider": "google",
        "input_per_million": 0.0375,
        "output_per_million": 0.15
    },

    "gemini-2.5-flash": {
        "provider": "google",
        "input_per_million": 0.30,
        "output_per_million": 2.50
    },

    "gemini-2.5-pro": {
        "provider": "google",
        "input_per_million": 1.25,
        "output_per_million": 10.00
    }
}
```


---

# FILE: app\services\provider_manager.py

```python
from app.services.providers.google_provider import (
    GoogleProvider
)


class ProviderManager:

    def __init__(self):

        self.providers = {
            "google": GoogleProvider()
        }

    def generate(
        self,
        provider_name: str,
        model_name: str,
        prompt: str
    ):

        provider = self.providers.get(
            provider_name
        )

        if not provider:

            raise ValueError(
                f"Provider not found: {provider_name}"
            )

        return provider.generate(
            model_name=model_name,
            prompt=prompt
        )


provider_manager = ProviderManager()
```


---

# FILE: app\services\provider_router.py

```python
from typing import Dict


class ProviderRouter:

    def select_provider(
        self,
        intent: str,
        risk_level: str,
        prompt_quality_score: int
    ) -> Dict:

        if risk_level == "HIGH":
            return {
                "provider": "local-secure-model",
                "reason": "Sensitive workload"
            }

        if intent == "SUMMARIZATION":
            return {
                "provider": "gemini-1.5-flash-8b",
                "reason": "Low-cost summarization"
            }

        if intent == "CODING":
            return {
                "provider": "advanced-code-model",
                "reason": "Optimized for coding"
            }

        if prompt_quality_score < 50:
            return {
                "provider": "quality-review-pipeline",
                "reason": "Prompt quality too low"
            }

        return {
            "provider": "gemini-1.5-flash",
            "reason": "General workload"
        }

```


---

# FILE: app\services\realtime_metrics.py

```python
from collections import defaultdict
from datetime import datetime


class RealtimeMetricsStore:

    def __init__(self):

        self.metrics = defaultdict(int)

        self.last_updated = datetime.utcnow()

    def increment_requests(self):

        self.metrics["total_requests"] += 1

        self.last_updated = datetime.utcnow()

    def add_tokens(self, tokens: int):

        self.metrics["total_tokens"] += tokens

        self.last_updated = datetime.utcnow()

    def add_cost(self, cost: float):

        self.metrics["total_cost"] += cost

        self.last_updated = datetime.utcnow()

    def add_high_risk(self):

        self.metrics["high_risk_requests"] += 1

        self.last_updated = datetime.utcnow()

    def get_metrics(self):

        return {
            **self.metrics,
            "last_updated": str(self.last_updated)
        }


metrics_store = RealtimeMetricsStore()
```


---

# FILE: app\services\__init__.py

```python

```


---

# FILE: app\services\providers\google_provider.py

```python
import google.generativeai as genai

from google.api_core.exceptions import (
    NotFound
)

from app.core.config import settings


# =========================================================
# GOOGLE PROVIDER
# =========================================================

class GoogleProvider:

    def __init__(self):

        genai.configure(
            api_key=settings.GEMINI_API_KEY
        )

        # =================================================
        # MODEL FALLBACK PRIORITY
        # =================================================

        self.fallback_models = [
            "gemini-3.5-flash",
            "gemini-1.5-flash-8b",
            "gemini-1.5-flash",
            "gemini-1.5-pro",
            "gemini-pro"
        ]

    # =====================================================
    # MODEL EXECUTION
    # =====================================================

    def generate(
        self,
        model_name: str,
        prompt: str
    ):

        tried_models = []

        models_to_try = [
            model_name
        ] + [
            m for m in self.fallback_models
            if m != model_name
        ]

        last_error = None

        for candidate_model in models_to_try:

            try:

                tried_models.append(
                    candidate_model
                )

                model = genai.GenerativeModel(
                    model_name=candidate_model
                )

                response = model.generate_content(
                    prompt
                )

                response_text = (
                    response.text
                    if hasattr(response, "text")
                    else str(response)
                )

                input_tokens = len(
                    prompt.split()
                )

                output_tokens = len(
                    response_text.split()
                )

                total_tokens = (
                    input_tokens
                    + output_tokens
                )

                return {

                    "provider": "google",

                    "model": candidate_model,

                    "response": response_text,

                    "input_tokens": (
                        input_tokens
                    ),

                    "output_tokens": (
                        output_tokens
                    ),

                    "total_tokens": (
                        total_tokens
                    ),

                    "fallback_used": (
                        candidate_model
                        != model_name
                    ),

                    "tried_models": (
                        tried_models
                    )
                }

            except NotFound as error:

                last_error = error

                continue

            except Exception as error:

                last_error = error

                continue

        raise RuntimeError(
            f"All Gemini models failed. "
            f"Tried models: {tried_models}. "
            f"Last error: {str(last_error)}"
        )
```


---

# FILE: app\utils\__init__.py

```python

```

