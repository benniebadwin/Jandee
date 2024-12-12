from django.db import models

class Branch(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class TransactionReport(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name="reports")
    month = models.DateField(help_text="Select the first day of the reporting month")
    cash_sales = models.DecimalField(max_digits=10, decimal_places=2)
    mpesa_sales = models.DecimalField(max_digits=10, decimal_places=2)
    branch_expense = models.DecimalField(max_digits=10, decimal_places=2)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    reliever_salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    airtime = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    other_expense_reason = models.TextField(null=True, blank=True)
    other_expense_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # Fields for payment proof
    bankslip_proof = models.ImageField(upload_to="bankslip_proofs/", null=True, blank=True)
    mpesa_transaction_message = models.TextField(null=True, blank=True, help_text="Paste the Mpesa transaction message here")

    # Calculated fields
    total_sales = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    total_banking = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        # Calculate total sales
        self.total_sales = self.cash_sales + self.mpesa_sales

        # Calculate total banking
        other_expense = self.other_expense_amount or 0
        reliever = self.reliever_salary or 0
        airtime = self.airtime or 0
        self.total_banking = (
            self.cash_sales
            - self.branch_expense
            - other_expense
            - self.salary
            - reliever
            - airtime
        )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.branch.name} - {self.month.strftime('%B, %Y')}"
