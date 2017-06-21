from django.shortcuts import render

from portal.forms import SignUpForm


def index(request, position="child", popup=None):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # ToDo: Spam protection - limit the number of requests before the user gets ignored
            # ToDo: Check if the username provided looks valid using RegEx
            # ToDo: Check if student exists and if he does then tell him to check his email

            student = form.save(commit=False)
            student.child = position == "child"
            student.save()

            # ToDo: Send email with magic link to student - use the function underneath to get the contents

            popup = student.get_new_student_popup()
    else:
        form = SignUpForm()

    return render(request, 'portal/index.html', {'position': position, 'form': form, 'popup': popup})


def preferences(request, id):
    return render(request, 'portal/preferences.html')
