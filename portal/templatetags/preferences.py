from django.template.defaulttags import register

from portal.forms import PartnerForm, PreferenceForm
from portal.models import Student, Family


@register.inclusion_tag('portal/partner_preferences.html')
def partner_preferences(student, partner_popup):
    offer = Student.objects.filter(partner=student)
    partner = PartnerForm(instance=student)

    return {'student': student, 'partner': partner, 'offer': offer, 'partner_popup': partner_popup}


@register.inclusion_tag('portal/personal_preferences.html')
def personal_preferences(student, preferences_popup):
    return {'preference': PreferenceForm(instance=student), 'preferences_popup': preferences_popup}


@register.inclusion_tag('portal/family_view.html')
def parents_view(student):
    return {'others': student.family.parents.all(), 'type': 'parents'}


@register.inclusion_tag('portal/family_view.html')
def children_view(student):
    return {'others': student.family.children.all(), 'type': 'children'}


@register.inclusion_tag('portal/family_view.html')
def sibling_view(student):
    return {'others': student.family.children.all().exclude(username=student.username), 'type': 'siblings'}

