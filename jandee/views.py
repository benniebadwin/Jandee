from django.shortcuts import render, redirect
from .models import TransactionReport, Branch
from .forms import TransactionReportForm
from django.shortcuts import render, redirect
from .forms import AddBranchForm
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
# views.py
from django.http import HttpResponse
from django.shortcuts import render
from .models import TransactionReport

# jandee/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import TransactionReport
from .forms import TransactionReportForm
from django.contrib.auth import logout


@login_required
def add_branch(request):
    if request.method == "POST":
        form = AddBranchForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("branch_list")  # Redirect to branch list after successful creation
    else:
        form = AddBranchForm()

    return render(request, "admin/add_branch.html", {"form": form})


def submit_report(request):
    if request.method == "POST":
        form = TransactionReportForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the cleaned data to the model
            transaction = form.save(commit=False)

            # Ensure the month and year are stored as a date
            month = int(form.cleaned_data["month"])
            year = int(form.cleaned_data["year"])
            transaction.month = f"{year}-{month:02d}-01"  # Store as the first day of the month

            transaction.save()
            return redirect("report_success")
        else:
            # If form is invalid, display errors
            return render(request, "reports/submit_report.html", {"form": form})
    else:
        # Initial form rendering
        form = TransactionReportForm()
    return render(request, "reports/submit_report.html", {"form": form})

def report_success(request):
    return render(request, "reports/success.html")



@login_required
def view_transactions(request):
    transactions = TransactionReport.objects.all()  # Get all transactions
    return render(request, 'admin/view_transactions.html', {'transactions': transactions})





@login_required
def view_sms_text(request, transaction_id):
    try:
        # Retrieve the transaction using the transaction ID
        transaction = TransactionReport.objects.get(id=transaction_id)

        # Check if there is an SMS message associated with this transaction
        if transaction.mpesa_transaction_message:
            # Return the SMS message in an HTTP response
            return HttpResponse(f"SMS Text: {transaction.mpesa_transaction_message}")
        else:
            # Return a message if there is no SMS text
            return HttpResponse("No SMS message available for this transaction.")
    except TransactionReport.DoesNotExist:
        return HttpResponse("Transaction not found.")





def edit_transaction(request, id):
    # Get the transaction report by ID
    transaction = get_object_or_404(TransactionReport, id=id)
    if request.method == 'POST':
        form = TransactionReportForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect('view_transactions')  # Redirect to view_transactions after saving
    else:
        form = TransactionReportForm(instance=transaction)
    return render(request, 'admin/edit_transaction.html', {'form': form})






@login_required
def branch_list(request):
    branches = Branch.objects.all()  # Get all Branches
    return render(request, 'admin/branch_list.html', {'branches': branches})

from .forms import AddBranchForm

def edit_branch(request, branch_id):
    branch = get_object_or_404(Branch, id=branch_id)
    
    if request.method == 'POST':
        form = AddBranchForm(request.POST, instance=branch)
        if form.is_valid():
            form.save()
            return redirect('branch_list')  # Redirect back to the branch list after editing
    else:
        form = AddBranchForm(instance=branch)
    
    return render(request, 'admin/edit_branch.html', {'form': form, 'branch': branch})


@login_required
def delete_branch(request, branch_id):
    # Fetch the branch object by ID
    branch = get_object_or_404(Branch, id=branch_id)

    # Check if the user has permission to delete, or use any other condition you want
    if not request.user.is_staff:
        return HttpResponseForbidden("You do not have permission to delete this branch.")

    # Perform the deletion
    branch.delete()

    # Redirect to the branch list view after deletion
    return redirect('branch_list')


def custom_logout(request):
    logout(request)  # Logs the user out
    return redirect('/') 