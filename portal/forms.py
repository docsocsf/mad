from django import forms
from django.core.exceptions import ValidationError

from portal.models import Student, Hobby


class SignUpForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['username']
        widgets = {
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

        # ToDo(martinzlocha): Filter the potential partner - remove self and people with requests/accepted

    def get_successful_proposal_popup(self):
        message = "Proposal has been successfully sent to %s." % self.cleaned_data['partner']
        return {'message': message, 'state': 'success'}
