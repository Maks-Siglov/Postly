from django import forms

from users.models import User


class ResetPasswordEmailForm(forms.Form):
    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'Account with this email does not exist'
            )

        return email
