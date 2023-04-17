class ApprovalCalculator:
    @staticmethod
    def is_approved(application, risk_score):
        # Loan approval criteria based on risk score
        if risk_score < 30:
            return True
        elif risk_score < 60:
            if application.loan_purpose != "debt_consolidation":
                return True
        return False
