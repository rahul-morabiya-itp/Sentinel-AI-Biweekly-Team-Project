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
