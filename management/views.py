from django.http import HttpResponse
from django.template import loader
from .models import Loans,Customers,Books
from django.contrib.auth.decorators import login_required
from .forms import CustomerForm, BookForm, LoanForm
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib import messages
from datetime import datetime,timedelta

def list_menu(request):
    context=None
    html_template = loader.get_template('list_menu.html')
    return HttpResponse(html_template.render(context,request))

@login_required(login_url='/accounts/login/')
def add_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Customer added successfully.')
            return redirect(reverse('list_menu'))
            
        else:
            messages.error(request,'Validation error')
            form = CustomerForm()
            context={'form':form}
            html_template = loader.get_template('create_customer.html')
            return HttpResponse(html_template.render(context, request))
    else:
        form = CustomerForm()
        context={'form':form}
        html_template = loader.get_template('create_customer.html')
        return HttpResponse(html_template.render(context, request))

@login_required(login_url='/accounts/login/')
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Book added successfully.')
            return redirect(reverse('list_menu'))
            
        else:
            messages.error(request,'Validation error')
            form = BookForm()
            context={'form':form}
            html_template = loader.get_template('add_book.html')
            return HttpResponse(html_template.render(context, request))
    else:
        form = BookForm()
        context={'form':form}
        html_template = loader.get_template('add_book.html')
        return HttpResponse(html_template.render(context, request))

@login_required(login_url='/accounts/login/')
def loan_book(request):
    if request.method == 'POST':
        form = LoanForm(request.POST)
        if form.is_valid():            
            form.save()
            messages.success(request,'Book Loan added successfully.')
            return redirect(reverse('list_menu'))
            
        else:
            print('from err',form.errors)
            messages.error(request,'Validation error')
            form = LoanForm()
            context={'form':form}
            html_template = loader.get_template('loan_book.html')
            return HttpResponse(html_template.render(context, request))
    else:
        form = LoanForm()
        context={'form':form}
        html_template = loader.get_template('loan_book.html')
        return HttpResponse(html_template.render(context, request))


@login_required(login_url='/accounts/login/')
def active_loans(request):
    loans = Loans.objects.filter(return_date__isnull=True)
    context={'loans':loans}
    html_template = loader.get_template('active_loans.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url='/accounts/login/')
def return_book(request,id):
    if request.method == 'POST':
        loan_obj = Loans.objects.get(id=id)
        form = LoanForm(request.POST,instance=loan_obj)
        if form.is_valid():            
            form.save()
            messages.success(request,'Book returned successfully.')
            return redirect(reverse('list_menu'))
            
        else:
            messages.error(request,'Validation error')
            loan_obj = Loans.objects.get(id=id)
            form = LoanForm(instance=loan_obj)
            context={'form':form}
            html_template = loader.get_template('return_book.html')
            return HttpResponse(html_template.render(context, request))
    else:
        loan_obj = Loans.objects.get(id=id)
        form = LoanForm(instance=loan_obj)
        context={'form':form}
        html_template = loader.get_template('return_book.html')
        return HttpResponse(html_template.render(context, request))


@login_required(login_url='/accounts/login/')
def display_customers(request):
    query = request.GET.get('query',None)
    if query:
        customers = Customers.objects.filter(name__icontains=query)
    else:
        customers = Customers.objects.all()
    context={'customers':customers}
    html_template = loader.get_template('display_customers.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url='/accounts/login/')
def display_books(request):
    query = request.GET.get('query',None)
    if query:
        books = Books.objects.filter(name__icontains=query)
    else:
        books = Books.objects.all()
    context={'books':books}
    html_template = loader.get_template('display_books.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url='/accounts/login/')
def display_loans(request):
    loans = Loans.objects.all()
    context={'loans':loans}
    html_template = loader.get_template('display_loans.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url='/accounts/login/')
def display_late_loans(request):
    loans = Loans.objects.filter(return_date__isnull=True)
    late_loans=[]
    for loan in loans:
        if loan.book.type == Books.upto_10_days:
            if datetime.now()>(loan.loan_date + timedelta(days=10)).replace(tzinfo=None) :
                late_loans.append(loan)
                continue
        elif loan.book.type == Books.upto_5_days:
            if datetime.now()>(loan.loan_date + timedelta(days=5)).replace(tzinfo=None):
                late_loans.append(loan)
                continue
        elif loan.book.type == Books.upto_2_days:
            if datetime.now()>(loan.loan_date + timedelta(days=2)).replace(tzinfo=None):
                late_loans.append(loan)
                continue

    context={'loans':late_loans}
    html_template = loader.get_template('display_late_loans.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url='/accounts/login/')
def remove_customer(request,id):
        Customers.objects.get(id=id).delete()
        messages.success(request,'Customer removed successfully.')
        return redirect(reverse('list_menu'))

@login_required(login_url='/accounts/login/')
def remove_book(request,id):
        Books.objects.get(id=id).delete()
        messages.success(request,'Book removed successfully.')
        return redirect(reverse('list_menu'))