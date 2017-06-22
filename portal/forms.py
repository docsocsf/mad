from django import forms

from portal.models import Student


class BaseForm(forms.ModelForm):
    """
    Extends ModelForm by adding form-control class to all fields of all forms which extend BaseForm
    """
    def __init__(self, *args, **kwargs):
        super(BaseForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class SignUpForm(BaseForm):
    class Meta:
        model = Student
        fields = ['username']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'xy1217'}),
        }

    def clean_username(self):
        username = self.cleaned_data['username']

        # ToDo: Check if the username provided looks valid

        return username
