from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import redirect, render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from leave_management.models import Leave

from .models import Employee
from .serializers import EmployeeSerializer


def _create_or_link_user(employee, username=None, password=None):
    if employee.user:
        return employee.user

    username_value = (username or '').strip()
    if not username_value:
        username_value = f"emp{employee.employee_id or employee.id}"

    username_value = ''.join(ch for ch in username_value if ch.isalnum() or ch in {'_', '.'})
    username_value = username_value.lower()

    if User.objects.filter(username=username_value).exists():
        username_value = f"{username_value}{employee.id or employee.employee_id}"

    password_value = password or 'Employee@123'
    user = User.objects.create_user(username=username_value, email=employee.email, password=password_value)
    employee.user = user
    employee.save(update_fields=['user'])
    return user


def login_page(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('home')
        return redirect('employee_dashboard')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('home')
            return redirect('employee_dashboard')

        return render(request, 'employee/login.html', {'error_message': 'Invalid username or password.'})

    return render(request, 'employee/login.html')


def user_logout(request):
    logout(request)
    return redirect('login_page')


def home_view(request):
    return render(request, 'employee/home.html')


@login_required
def insert_view(request):
    if not request.user.is_superuser:
        return redirect('employee_dashboard')

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
            date_of_joining=date_of_joining,
        )
        employee.save()

        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        _create_or_link_user(employee, username=username, password=password)

        return redirect('display')

    return render(request, 'employee/insert.html', {'msg': 'Employee created successfully.'})


@login_required
def display_view(request):
    if not request.user.is_superuser:
        return redirect('employee_dashboard')

    search = request.GET.get('search')

    if search:
        if search.isdigit():
            employees = Employee.objects.filter(Q(employee_id=int(search)) | Q(name__icontains=search))
        else:
            employees = Employee.objects.filter(name__icontains=search)
    else:
        employees = Employee.objects.all()

    context = {'employees': employees}
    return render(request, 'employee/display.html', context)


@login_required
def update_view(request, id):
    if not request.user.is_superuser:
        return redirect('employee_dashboard')

    employee = Employee.objects.get(id=id)

    if request.method == 'POST':
        employee.employee_id = request.POST.get('employee_id')
        employee.name = request.POST.get('name')
        employee.email = request.POST.get('email')
        employee.department = request.POST.get('department')
        employee.mobile_number = request.POST.get('mobile_number')
        employee.date_of_joining = request.POST.get('date_of_joining')
        employee.save()

        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        if username or password:
            _create_or_link_user(employee, username=username, password=password)

        return redirect('display')

    context = {'employee': employee}
    return render(request, 'employee/update.html', context)


@login_required
def delete_view(request, id):
    if not request.user.is_superuser:
        return redirect('employee_dashboard')

    employee = Employee.objects.get(id=id)
    employee.delete()
    return redirect('display')


@login_required
def dashboard_view(request):
    if not request.user.is_superuser:
        return redirect('employee_dashboard')

    total_employees = Employee.objects.count()
    total_leaves = Leave.objects.count()
    pending = Leave.objects.filter(status='Pending').count()
    approved = Leave.objects.filter(status='Approved').count()
    rejected = Leave.objects.filter(status='Rejected').count()

    context = {
        'total_employees': total_employees,
        'total_leaves': total_leaves,
        'pending': pending,
        'approved': approved,
        'rejected': rejected,
    }
    return render(request, 'employee/dashboard.html', context)


@login_required
def employee_dashboard(request):
    if request.user.is_superuser:
        return redirect('home')

    employee_profile = Employee.objects.filter(user=request.user).first()
    leaves = Leave.objects.filter(employee=employee_profile) if employee_profile else Leave.objects.none()

    context = {
        'employee_profile': employee_profile,
        'total_leaves': leaves.count(),
        'pending': leaves.filter(status='Pending').count(),
        'approved': leaves.filter(status='Approved').count(),
        'rejected': leaves.filter(status='Rejected').count(),
    }
    return render(request, 'employee/employee_dashboard.html', context)


# ===================== GET ALL =====================

@login_required
@api_view(['GET'])
def employee_list_api(request):
    if not request.user.is_superuser:
        return Response({'detail': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

    employees = Employee.objects.all()
    serializer = EmployeeSerializer(employees, many=True)
    return Response(serializer.data)


# ===================== GET ONE =====================

@login_required
@api_view(['GET'])
def employee_detail_api(request, id):
    if not request.user.is_superuser:
        return Response({'detail': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

    employee = Employee.objects.get(id=id)
    serializer = EmployeeSerializer(employee)
    return Response(serializer.data)


# ===================== POST =====================

@login_required
@api_view(['POST'])
def employee_create_api(request):
    if not request.user.is_superuser:
        return Response({'detail': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

    serializer = EmployeeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors)


# ===================== PUT =====================

@login_required
@api_view(['PUT'])
def employee_update_api(request, id):
    if not request.user.is_superuser:
        return Response({'detail': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

    employee = Employee.objects.get(id=id)
    serializer = EmployeeSerializer(employee, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)


# ===================== DELETE =====================

@login_required
@api_view(['DELETE'])
def employee_delete_api(request, id):
    if not request.user.is_superuser:
        return Response({'detail': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

    employee = Employee.objects.get(id=id)
    employee.delete()
    return Response({'message': 'Employee Deleted Successfully'})