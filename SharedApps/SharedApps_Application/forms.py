from django import forms
from SharedApps_Application.models import certificateDb
from SharedApps_Application.models import serviceDb
from django.contrib.admin.widgets import AdminDateWidget
from django.forms.fields import DateField

def validate_file_extension(value):
        if not value.name.endswith('.csr'):
            raise forms.ValidationError("Only CSR file is accepted")

class CertificateForm(forms.ModelForm):
    app_attributes = {'oninvalid': 'this.setCustomValidity("Application field is required")', 'oninput': 'this.setCustomValidity("")'}
    startdate = forms.DateField(widget = forms.SelectDateWidget(years=range(1995, 2100)))
    expiredate = forms.DateField(widget = forms.SelectDateWidget(years=range(1995, 2100)))
    application = forms.CharField(widget=forms.TextInput(attrs=app_attributes))
    File= forms.FileField(required=True,validators=[validate_file_extension])
    class Meta:
        model = certificateDb
        fields = ('application', 'startdate', 'expiredate', 'environment_type','File' )

        error_messages = {
            'application': {
                'required': ("Application field is required"),
            },
            }
    def clean(self):
        cleaned_data = super().clean() 
        startdate = cleaned_data.get("startdate")
        expiredate = cleaned_data.get("expiredate")
        if expiredate < startdate:
            msg = u"expiredate should be greater than startdate."
            raise forms.ValidationError(msg,  code="invalid")






class serviceForm(forms.ModelForm):
    app_attributes = {'oninvalid': 'this.setCustomValidity("Application field is required")', 'oninput': 'this.setCustomValidity("")'}
    startdate = forms.DateField(widget = forms.SelectDateWidget(years=range(1995, 2100)))
    expiredate = forms.DateField(widget = forms.SelectDateWidget(years=range(1995, 2100)))
    application = forms.CharField(widget=forms.TextInput(attrs=app_attributes))

    class Meta:
        model = serviceDb
        fields = ('application', 'startdate', 'expiredate', 'environment_type' )

        error_messages = {
            'application': {
                'required': ("Application field is required"),
            },
            }
    def clean(self):
        cleaned_data = super().clean() 
        startdate = cleaned_data.get("startdate")
        expiredate = cleaned_data.get("expiredate")
        if expiredate < startdate:
            msg = u"expiredate should be greater than startdate."
            raise forms.ValidationError(msg,  code="invalid")

