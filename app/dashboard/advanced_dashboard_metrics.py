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
