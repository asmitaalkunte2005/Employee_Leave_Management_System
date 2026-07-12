from django.shortcuts import render, redirect
from .models import Leave
from employee.models import Employee
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import LeaveSerializer

# ---------------- APPLY LEAVE ----------------

def apply_leave(request):

    employees = Employee.objects.all()
    context = {"employees": employees}

    if request.method == "POST":

        employee_id = request.POST.get("employee")
        leave_type = request.POST.get("leave_type")
        from_date = request.POST.get("from_date")
        to_date = request.POST.get("to_date")
        reason = request.POST.get("reason")
        status = request.POST.get("status")

        employee = Employee.objects.get(id=employee_id)

        leave = Leave(
            employee=employee,
            leave_type=leave_type,
            from_date=from_date,
            to_date=to_date,
            reason=reason,
            status=status
        )

        leave.save()

        return redirect('display_leave')

    return render(request, "leave_management/apply_leave.html", context)


# ---------------- DISPLAY LEAVE ----------------

from django.db.models import Q

def display_leave(request):

    status = request.GET.get("status")
    leave_type = request.GET.get("leave_type")

    leaves = Leave.objects.all()

    if status:
        leaves = leaves.filter(status=status)

    if leave_type:
        leaves = leaves.filter(leave_type=leave_type)

    context = {
        "leaves": leaves
    }

    return render(request, "leave_management/display_leave.html", context)


# ---------------- UPDATE LEAVE ----------------

def update_leave(request, id):

    leave = Leave.objects.get(id=id)
    employees = Employee.objects.all()

    if request.method == "POST":

        employee_id = request.POST.get("employee")

        leave.employee = Employee.objects.get(id=employee_id)
        leave.leave_type = request.POST.get("leave_type")
        leave.from_date = request.POST.get("from_date")
        leave.to_date = request.POST.get("to_date")
        leave.reason = request.POST.get("reason")
        leave.status = request.POST.get("status")

        leave.save()

        return redirect('display_leave')

    context = {
        "leave": leave,
        "employees": employees
    }

    return render(request, "leave_management/update_leave.html", context)


# ---------------- DELETE LEAVE ----------------

def delete_leave(request, id):

    leave = Leave.objects.get(id=id)

    leave.delete()

    leaves = Leave.objects.all()

    context = {
        "leaves": leaves
    }

    return render(request, "leave_management/display_leave.html", context)







# ================= GET ALL =================

@api_view(['GET'])
def leave_list_api(request):

    leaves = Leave.objects.all()

    serializer = LeaveSerializer(leaves, many=True)

    return Response(serializer.data)


# ================= GET ONE =================

@api_view(['GET'])
def leave_detail_api(request, id):

    leave = Leave.objects.get(id=id)

    serializer = LeaveSerializer(leave)

    return Response(serializer.data)


# ================= POST =================

@api_view(['POST'])
def leave_create_api(request):

    serializer = LeaveSerializer(data=request.data)

    if serializer.is_valid():

        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors)


# ================= PUT =================

@api_view(['PUT'])
def leave_update_api(request, id):

    leave = Leave.objects.get(id=id)

    serializer = LeaveSerializer(leave, data=request.data)

    if serializer.is_valid():

        serializer.save()

        return Response(serializer.data)

    return Response(serializer.errors)


# ================= DELETE =================

@api_view(['DELETE'])
def leave_delete_api(request, id):

    leave = Leave.objects.get(id=id)

    leave.delete()

    return Response({"message": "Leave Deleted Successfully"})