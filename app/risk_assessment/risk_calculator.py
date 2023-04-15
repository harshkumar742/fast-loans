class RiskCalculator:
    @staticmethod
    def calculate_risk(application):
        risk_score = 0

        # Credit score impact
        credit_score = application.credit_score
        if credit_score < 600:
            risk_score += 30
        elif credit_score < 700:
            risk_score += 20
        elif credit_score < 800:
            risk_score += 10

        # Debt-to-income ratio impact
        dti = application.monthly_debt / application.monthly_income
        if dti > 0.43:
            risk_score += 30
        elif dti > 0.36:
            risk_score += 20
        elif dti > 0.28:
            risk_score += 10

        # Employment status impact
        employment_status = application.employment_status
        if employment_status.lower() == "unemployed":
            risk_score += 20
        elif employment_status.lower() == "self-employed":
            risk_score += 10

        # Loan amount and purpose impact
        loan_amount = application.loan_amount
        loan_purpose = application.loan_purpose.lower()
        if loan_purpose == "business":
            risk_score += 10
        elif loan_purpose == "education":
            risk_score += 5
        elif loan_purpose == "debt_consolidation":
            risk_score += 15

        # Loan-to-income ratio impact
        loan_to_income = loan_amount / application.monthly_income
        if loan_to_income > 0.5:
            risk_score += 20
        elif loan_to_income > 0.3:
            risk_score += 10

        return risk_score
