from django import forms
from .models import Employee

class EmployeeForm(forms.ModelForm):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'placeholder': 'Enter Employee\'s Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': '*******'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': '*******'}))
    email = forms.EmailField(max_length=60, widget=forms.EmailInput(attrs={'placeholder': 'employee@yourcompany.com'}))

    class Meta:
        model = Employee
        fields = [
            'username', 'full_name', 'email',
            'department' ,'password', 'confirm_password'
        ]

        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Enter Employee\'s Full Name'}),
            'department': forms.TextInput(attrs={'placeholder': 'Enter Employee\'s Department'}),
        }


    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})