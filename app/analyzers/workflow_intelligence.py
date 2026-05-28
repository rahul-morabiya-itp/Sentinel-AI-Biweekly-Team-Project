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
