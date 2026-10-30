from django.shortcuts import render, redirect
from .forms import StudentForm
from .models import Student

# Create your views here.
def student_list(request):
    students = Student.objects.all()


    context = {
        'Students': students,
    }

    return render(request, 'list.html', context)

def student_create(request):

    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("students:student_list")

    form = StudentForm()

    context = {
        'form': form,
        'title': 'Add New Student',
    }

    return render(request, 'form.html', context)