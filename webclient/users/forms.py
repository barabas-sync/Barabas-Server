from django import forms
import webserver
from lib.identity.user import User
from lib.identity.passwordauthentication import PasswordAuthentication

class PasswordLoginForm(forms.Form):
    username = forms.CharField(max_length = 32, label = "Username")
    password = forms.CharField(widget=forms.PasswordInput, label = "Password")
    
    def clean(self):
        """Empty docstring"""
        data = self.cleaned_data
        db = webserver.WebServer.database()
        pa = db.find(PasswordAuthentication, PasswordAuthentication.username == data['username']).one()
        
        if not (pa and pa.testPassword(data['password'])):
            raise forms.ValidationError("Wrong username or password")
        
        data['passwordAuthentication'] = pa
        return data

class PasswordBasedRegistrationForm(forms.Form):
    username = forms.CharField(max_length = 32, label = "Username")
    email = forms.CharField(label = "E-mail")
    firstName = forms.CharField(label = "First Name")
    lastName = forms.CharField(label = "Last Name")
    
    password = forms.CharField(widget = forms.PasswordInput, label = "Password")
    passwordCheck = forms.CharField(widget = forms.PasswordInput, label = "Password (check)")
    
    def clean(self):
        """Empty docstring"""
        data = self.cleaned_data
        print data['password']
        
        db = webserver.WebServer.database()
        user = User(data['firstName'], data['lastName'], data['email'])
        pa = PasswordAuthentication()
        pa.username = data['username']
        pa.password(data['password'])
        pa.user = user
        
        data['user'] = user
        data['passwordAuth'] = pa
        return data

class ProfileForm(forms.Form):
    pass
    
