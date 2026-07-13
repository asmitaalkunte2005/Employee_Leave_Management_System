from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from employee.models import Employee

from .models import Leave
from .serializers import LeaveSerializer

# ---------------- APPLY LEAVE ----------------

@login_required
def apply_leave(request):
    if request.user.is_superuser:
        employees = Employee.objects.all()
    else:
        employee_profile = Employee.objects.filter(user=request.user).first()
        employees = Employee.objects.filter(id=employee_profile.id) if employee_profile else Employee.objects.none()

    context = {"employees": employees}

    if request.method == "POST":
        if request.user.is_superuser:
            employee_id = request.POST.get("employee")
        else:
            employee_profile = Employee.objects.filter(user=request.user).first()
            employee_id = employee_profile.id if employee_profile else None

        if employee_id is None:
            return redirect('employee_dashboard')

        leave_type = request.POST.get("leave_type")
        from_date = request.POST.get("from_date")
        to_date = request.POST.get("to_date")
        reason = request.POST.get("reason")
        requested_status = request.POST.get("status", "Pending")

        employee = Employee.objects.get(id=employee_id)

        leave = Leave(
            employee=employee,
            leave_type=leave_type,
            from_date=from_date,
            to_date=to_date,
            reason=reason,
            status=requested_status if request.user.is_superuser else 'Pending'
        )

        leave.save()

        return redirect('display_leave')

    return render(request, "leave_management/apply_leave.html", context)


# ---------------- DISPLAY LEAVE ----------------

@login_required
def display_leave(request):
    status = request.GET.get("status")
    leave_type = request.GET.get("leave_type")

    if request.user.is_superuser:
        leaves = Leave.objects.all()
    else:
        leaves = Leave.objects.filter(employee__user=request.user)

    if status:
        leaves = leaves.filter(status=status)

    if leave_type:
        leaves = leaves.filter(leave_type=leave_type)

    context = {
        "leaves": leaves
    }

    return render(request, "leave_management/display_leave.html", context)


# ---------------- UPDATE LEAVE ----------------

@login_required
def update_leave(request, id):
    leave = Leave.objects.get(id=id)

    if not request.user.is_superuser and (leave.employee.user_id != request.user.id or leave.status != 'Pending'):
        return redirect('employee_dashboard')

    employees = Employee.objects.all() if request.user.is_superuser else Employee.objects.filter(user=request.user)

    if request.method == "POST":
        if request.user.is_superuser:
            employee_id = request.POST.get("employee")
            leave.employee = Employee.objects.get(id=employee_id)
            leave.status = request.POST.get("status", leave.status)
        else:
            leave.employee = Employee.objects.get(id=leave.employee.id)
            leave.status = 'Pending'

        leave.leave_type = request.POST.get("leave_type")
        leave.from_date = request.POST.get("from_date")
        leave.to_date = request.POST.get("to_date")
        leave.reason = request.POST.get("reason")
        leave.save()

        return redirect('display_leave')

    context = {
        "leave": leave,
        "employees": employees
    }

    return render(request, "leave_management/update_leave.html", context)


# ---------------- DELETE LEAVE ----------------

@login_required
def delete_leave(request, id):
    leave = Leave.objects.get(id=id)

    if not request.user.is_superuser and (leave.employee.user_id != request.user.id or leave.status != 'Pending'):
        return redirect('employee_dashboard')

    leave.delete()
    return redirect('display_leave')







# ================= GET ALL =================

@login_required
@api_view(['GET'])
def leave_list_api(request):
    if not request.user.is_superuser:
        return Response({'detail': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

    leaves = Leave.objects.all()

    serializer = LeaveSerializer(leaves, many=True)

    return Response(serializer.data)


# ================= GET ONE =================

@login_required
@api_view(['GET'])
def leave_detail_api(request, id):
    if not request.user.is_superuser:
        return Response({'detail': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

    leave = Leave.objects.get(id=id)

    serializer = LeaveSerializer(leave)

    return Response(serializer.data)


# ================= POST =================

@login_required
@api_view(['POST'])
def leave_create_api(request):
    if not request.user.is_superuser:
        return Response({'detail': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

    serializer = LeaveSerializer(data=request.data)

    if serializer.is_valid():

        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors)


# ================= PUT =================

@login_required
@api_view(['PUT'])
def leave_update_api(request, id):
    if not request.user.is_superuser:
        return Response({'detail': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

    leave = Leave.objects.get(id=id)

    serializer = LeaveSerializer(leave, data=request.data)

    if serializer.is_valid():

        serializer.save()

        return Response(serializer.data)

    return Response(serializer.errors)


# ================= DELETE =================

@login_required
@api_view(['DELETE'])
def leave_delete_api(request, id):
    if not request.user.is_superuser:
        return Response({'detail': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

    leave = Leave.objects.get(id=id)

    leave.delete()

    return Response({"message": "Leave Deleted Successfully"})