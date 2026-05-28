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