from django.shortcuts import render, redirect, get_object_or_404
from .forms import StudentForm
from .models import Student
from django.contrib import messages

# Create your views here.
def student_list(request):
    students = Student.objects.all()


    context = {
        'students': students,
    }

    return render(request, 'list.html', context)

# create button----------------------------------------------
def student_create(request):

    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
           student =  form.save()
           messages.success(request, f"Student {student} was created successfully")
           return redirect("students:student_profile", pk=student.pk)
    else:
        form = StudentForm()

    context = {
        'form': form,
        'title': 'Add New Student',
    }

    return render(request, 'form.html', context)

# edit button------------------------
def student_edit(request, pk):

    student = get_object_or_404(Student, pk=pk) #for error display incase the field is not selected

    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            student = form.save()
            messages.success(request, f"Student {student} was updated successfully")
            return redirect("students:student_profile", pk=student.pk)
    else:
        form = StudentForm(instance=student)

    context = {
        'form': form,
        'title': 'Update Student',
    }

    return render(request, 'form.html', context)

# for the delete button
def student_delete(request, pk):

    student = get_object_or_404(Student, pk=pk) #for error display incase the field is not selected

    if request.method == "POST":
        student.delete()
        messages.success(request, f"Student {student} was deleted successfully")
        return redirect("students:student_list")

def student_profile(request, pk):

    student = get_object_or_404(Student, pk=pk) #for error display incase the field is not selected

    context = {
        'student': student,
    }


    return render(request, "profile.html", context)