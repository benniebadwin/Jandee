import datetime
from django import forms
from .models import TransactionReport
from .models import Branch

class AddBranchForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = ['name']  # Only include the name field
        # Add customizations if needed

class TransactionReportForm(forms.ModelForm):
    # Additional fields for month and year selection
    month = forms.ChoiceField(
        choices=[(i, datetime.date(1900, i, 1).strftime("%B")) for i in range(1, 13)],
        label="Month",
    )
    year = forms.ChoiceField(
        choices=[(y, y) for y in range(datetime.date.today().year - 5, datetime.date.today().year + 1)],
        label="Year",
    )

    class Meta:
        model = TransactionReport
        fields = [
            "branch",
            "cash_sales",
            "mpesa_sales",
            "branch_expense",
            "salary",
            "reliever_salary",
            "airtime",
            "other_expense_reason",
            "other_expense_amount",
            "bankslip_proof",
            "mpesa_transaction_message",
        ]

    def clean(self):
        cleaned_data = super().clean()
        month = cleaned_data.get("month")
        year = cleaned_data.get("year")

        if not month or not year:
            raise forms.ValidationError("Both month and year must be provided.")

        try:
            cleaned_data["month"] = int(month)
            cleaned_data["year"] = int(year)
        except ValueError:
            raise forms.ValidationError("Invalid month or year provided.")

        return cleaned_data