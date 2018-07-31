from django import forms

from user.models import User


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['nickname', 'password', 'icon', 'age', 'sex']

    password2 = forms.CharField(max_length=128)


    def clean_password2(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")
        print(password)
        print(password2)

        if password != password2:
            raise forms.ValidationError("两次密码不一致")

        if len(password) < 6:
            raise forms.ValidationError('密码太简单')



