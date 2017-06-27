from django.shortcuts import render, get_object_or_404

from portal.forms import SignUpForm, PreferenceForm
from portal.models import Student
from portal.utils import get_invalid_id_popup


def index(request, position="child", popup=None):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # ToDo(martinzlocha): Spam protection - limit the number of requests before the user gets ignored
            # ToDo(martinzlocha): Check if student exists and if he does then tell him to check his email

            student = form.save(commit=False)
            student.child = position == "child"
            student.save()

            # ToDo(martinzlocha): Send email with magic link to student

            popup = student.get_new_student_popup()
    else:
        form = SignUpForm()

    return render(request, 'portal/index.html', {'position': position, 'form': form, 'popup': popup})


def preferences(request, id):
    if not Student.objects.filter(magic_id=id).exists():
        return index(request, popup=get_invalid_id_popup())

    instance = Student.objects.get(magic_id=id)

    if request.method == 'POST':
        form = PreferenceForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
    else:
        form = PreferenceForm(instance=instance)

    return render(request, 'portal/preferences.html', {'form': form})
