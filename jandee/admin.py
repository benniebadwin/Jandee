from django.contrib import admin
from .models import Branch, TransactionReport
from django.contrib import admin
from .models import Branch, TransactionReport

class BranchAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class TransactionReportAdmin(admin.ModelAdmin):
    list_display = ('branch', 'month', 'cash_sales', 'mpesa_sales', 'branch_expense', 'salary', 'reliever_salary', 'airtime')
    search_fields = ('branch__name',)

admin.site.register(Branch, BranchAdmin)
admin.site.register(TransactionReport, TransactionReportAdmin)




# @admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ("name",)

# @admin.register(TransactionReport)
class TransactionReportAdmin(admin.ModelAdmin):
    list_display = (
        "branch",
        "month",
        "cash_sales",
        "mpesa_sales",
        "total_sales",
        "total_banking",
    )
    list_filter = ("branch", "month")
    search_fields = ("branch__name",)
    readonly_fields = ("total_sales", "total_banking")
    fieldsets = (
        ("Basic Information", {
            "fields": ("branch", "month"),
        }),
        ("Sales and Expenses", {
            "fields": (
                "cash_sales",
                "mpesa_sales",
                "branch_expense",
                "salary",
                "reliever_salary",
                "airtime",
                "other_expense_reason",
                "other_expense_amount",
            ),
        }),
        ("Payment Proof", {
            "fields": ("bankslip_proof", "mpesa_transaction_message"),
        }),
        ("Calculated Totals", {
            "fields": ("total_sales", "total_banking"),
        }),
    )

