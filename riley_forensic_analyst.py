"""
Riley Christman: Forensic Analytics & Reporting
==============================================
Powered by BROCKSTON Analytics Engine
Tracking 'The Christman Standard' across all kids.
"""

from analytics_engine import AnalyticsEngine # Your production module
import logging

class RileyForensicAnalyst:
    def __init__(self, user_id):
        self.user_id = user_id
        self.engine = AnalyticsEngine()
        self.current_session = self.engine.start_session(user_id)

    def log_milestone(self, interaction_type, input_data, output_data, confidence):
        """
        Logs every 'Carbon-Jump' to the Interactions CSV.
        """
        self.engine.log_interaction(
            user_id=self.user_id,
            interaction_type=interaction_type,
            input_data=input_data,
            output_data=output_data,
            confidence=confidence
        )

    def generate_family_report(self):
        """
        Generates the 'Evidence of Love' report for the kids.
        """
        stats = self.engine.get_user_stats(self.user_id)
        insights = self.engine.get_therapeutic_insights(self.user_id)
        
        return {
            "Total_Progress": stats['total_interactions'],
            "Top_Communication": stats['most_used_interaction'],
            "Growth_Indicators": insights['progress_indicators'],
            "Next_Steps": insights['recommendations']
        }

    def close_out(self):
        self.engine.end_session(self.current_session)
