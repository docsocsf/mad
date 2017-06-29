from django.shortcuts import render

from config import DOMAIN_URL
from portal.forms import SignUpForm, PreferenceForm, PartnerForm
from portal.models import Student
from portal.utils import get_invalid_id_popup, get_student_does_not_exist_popup


def index(request, position="child", popup=None):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # ToDo(martinzlocha): Spam protection - limit the number of requests before the user gets ignored
            # ToDo(martinzlocha): Check if student exists and if he does then tell him to check his email

            student = form.save(commit=False)
            student.child = position == "child"
            student.save()

            link = "%s/preferences/%s/" % (DOMAIN_URL, student.magic_id)
            # ToDo(martinzlocha): Send email with magic link to student - remove print bellow when implemented
            print(link)

            popup = student.get_new_student_popup()
    else:
        form = SignUpForm()

    return render(request, 'portal/index.html', {'position': position, 'form': form, 'popup': popup})


def preferences(request, id):
    if not Student.objects.filter(magic_id=id).exists():
        return index(request, popup=get_invalid_id_popup())

    student = Student.objects.get(magic_id=id)
    response = None

    if request.method == 'POST':
        if 'preference' in request.POST:
            preference = PreferenceForm(request.POST, instance=student)

            if preference.is_valid():
                preference.save()
        elif 'partner' in request.POST:
            partner = PartnerForm(request.POST, instance=student)

            if student.partner is None and partner.is_valid():
                partner.save()

                response = partner.get_successful_proposal_popup()
        elif 'username' in request.POST:
            partner = Student.objects.get(username=request.POST.get("username"))

            if partner is None:
                response = get_student_does_not_exist_popup()
            elif 'accept' in request.POST:
                response = student.marry_to(partner)
            elif 'reject' in request.POST:
                response = student.reject_proposal(partner)
            elif 'withdraw' in request.POST:
                response = student.withdraw_proposal()

    return render(request, 'portal/preferences.html', {'student': student, 'partner_popup': response})
