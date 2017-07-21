from django import forms
from django.core.exceptions import ValidationError

from portal.models import Student, Hobby


class SignUpForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'username', 'gender', 'course']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ideally similar to name on FB'}),
            'username': forms.TextInput(attrs={'placeholder': 'xy1217'}),
        }

    def clean_username(self):
        username = self.cleaned_data['username']

        # ToDo(martinzlocha): Check if the username provided looks valid

        return username


class PreferenceForm(forms.ModelForm):
    hobbies = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(), required=False,
                                             queryset=Hobby.objects.all())

    class Meta:
        model = Student
        fields = ('party', 'hobbies')

    def __init__(self, *args, **kwargs):
        super(PreferenceForm, self).__init__(*args, **kwargs)
        self.fields['party'].label = "Do you enjoy clubbing/partying/drinking?"
        self.fields['hobbies'].label = "What are your hobbies? (Maximum 5 responses)"

    def clean_hobbies(self):
        hobbies = self.cleaned_data['hobbies']

        if len(hobbies) > 5:
            raise ValidationError("Maximum of 5 hobbies.")

        return hobbies


class PartnerForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('partner',)

    def __init__(self, *args, **kwargs):
        super(PartnerForm, self).__init__(*args, **kwargs)
        self.instance = kwargs.pop('instance', None)
        self.fields['partner'].help_text = "If you don't have a partner then one will be allocated to you with " \
                                           "similar hobbies."

        choice = Student.objects.filter(confirmed=False, child=False).exclude(username__contains=self.instance.username)
        self.fields["partner"].queryset = choice

    def get_successful_proposal_popup(self):
        message = "Proposal has been successfully sent to %s." % self.cleaned_data['partner']
        return {'message': message, 'state': 'success'}
