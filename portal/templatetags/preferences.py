from django.template.defaulttags import register

from portal.forms import PartnerForm, PreferenceForm
from portal.models import Student


@register.inclusion_tag('portal/partner_preferences.html')
def partner_preferences(student, partner_popup):
    offer = Student.objects.filter(partner=student)
    partner = PartnerForm(instance=student)

    return {'student': student, 'partner': partner, 'offer': offer, 'partner_popup': partner_popup}


@register.inclusion_tag('portal/personal_preferences.html')
def personal_preferences(student):
    return {'preference': PreferenceForm(instance=student)}
