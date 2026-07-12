from django.shortcuts import render,redirect
from .models import Employee
from leave_management.models import Leave
from django.db.models import Q
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import EmployeeSerializer


def home_view(request):
    return render(request, 'employee/home.html')

from django.shortcuts import render
from .models import Employee

def insert_view(request):

    context = {}

    if request.method == 'POST':

        employee_id = request.POST.get('employee_id')
        name = request.POST.get('name')
        email = request.POST.get('email')
        department = request.POST.get('department')
        mobile_number = request.POST.get('mobile_number')
        date_of_joining = request.POST.get('date_of_joining')

        employee = Employee(
            employee_id=employee_id,
            name=name,
            email=email,
            department=department,
            mobile_number=mobile_number,
            date_of_joining=date_of_joining
        )

        employee.save()

        return redirect('display')

    return render(request, 'employee/insert.html', context)


def display_view(request):

    employees = Employee.objects.all()

    context = {
        "employees": employees
    }

    return render(request, "employee/display.html", context)


def update_view(request, id):

    employee = Employee.objects.get(id=id)

    if request.method == "POST":

        employee.employee_id = request.POST.get('employee_id')
        employee.name = request.POST.get('name')
        employee.email = request.POST.get('email')
        employee.department = request.POST.get('department')
        employee.mobile_number = request.POST.get('mobile_number')
        employee.date_of_joining = request.POST.get('date_of_joining')

        employee.save()

        return redirect('display')

    context = {
        "employee": employee
    }

    return render(request, "employee/update.html", context)


from django.shortcuts import render
from .models import Employee

def delete_view(request, id):

    employee = Employee.objects.get(id=id)

    employee.delete()

    employees = Employee.objects.all()

    context = {
        "employees": employees
    }

    return render(request, "employee/display.html", context)


def dashboard_view(request):

    total_employees = Employee.objects.count()

    total_leaves = Leave.objects.count()

    pending = Leave.objects.filter(status="Pending").count()

    approved = Leave.objects.filter(status="Approved").count()

    rejected = Leave.objects.filter(status="Rejected").count()

    context = {
        "total_employees": total_employees,
        "total_leaves": total_leaves,
        "pending": pending,
        "approved": approved,
        "rejected": rejected,
    }

    return render(request, "employee/dashboard.html", context)



def display_view(request):

    search = request.GET.get("search")

    if search:

        if search.isdigit():
            employees = Employee.objects.filter(
                Q(employee_id=int(search)) |
                Q(name__icontains=search)
            )
        else:
            employees = Employee.objects.filter(
                name__icontains=search
            )

    else:
        employees = Employee.objects.all()

    context = {
        "employees": employees
    }

    return render(request, "employee/display.html", context)



# ===================== GET ALL =====================

@api_view(['GET'])
def employee_list_api(request):

    employees = Employee.objects.all()

    serializer = EmployeeSerializer(employees, many=True)

    return Response(serializer.data)


# ===================== GET ONE =====================

@api_view(['GET'])
def employee_detail_api(request, id):

    employee = Employee.objects.get(id=id)

    serializer = EmployeeSerializer(employee)

    return Response(serializer.data)


# ===================== POST =====================

@api_view(['POST'])
def employee_create_api(request):

    serializer = EmployeeSerializer(data=request.data)

    if serializer.is_valid():

        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors)


# ===================== PUT =====================

@api_view(['PUT'])
def employee_update_api(request, id):

    employee = Employee.objects.get(id=id)

    serializer = EmployeeSerializer(employee, data=request.data)

    if serializer.is_valid():

        serializer.save()

        return Response(serializer.data)

    return Response(serializer.errors)


# ===================== DELETE =====================

@api_view(['DELETE'])
def employee_delete_api(request, id):

    employee = Employee.objects.get(id=id)

    employee.delete()

    return Response({"message": "Employee Deleted Successfully"})