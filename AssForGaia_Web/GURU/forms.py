from django import forms

class WebSourceForm(forms.Form):
    rooturl = forms.IntegerField()
    host = forms.IntegerField()
    port = forms.IntegerField()
    webname = forms.IntegerField()
    webpsw = forms.IntegerField()    
class DbSourceForm(forms.Form):
    servername = forms.IntegerField()
    dbusername = forms.IntegerField()
    dbpsw = forms.IntegerField()
    dbname = forms.IntegerField()
    sourcename = forms.IntegerField()