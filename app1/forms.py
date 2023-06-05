from django.contrib.auth.forms import UserCreationForm
from app1.models import User


class CreateUserForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ['username','email','password1','password2']

    # for removing password2----->
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     del self.fields['password2']    