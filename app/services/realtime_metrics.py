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