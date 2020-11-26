from django import forms
dep=( 
    ("CSE", "Computer Science and Engineering"), 
    ("ECE", "Electronics and Communication Engineering"), 
    ("MECH", "Mechanical Engineering"), 
    ("EEE", "Electrical and Electronics Engineering"), 
    ("MECT", "Mechatronics"), 
    ("IT", "Information Technology"),
    ("CA", "Computer Application"),
    ("DS", "Data Science"),
    
) 
class PostRegisterForm(forms.Form):
    name = forms.CharField(max_length=20)
    regno = forms.CharField(max_length=6)
    email = forms.EmailField()
    phone = forms.CharField(max_length=12)
    dept = forms.ChoiceField(choices = dep)
    #event = forms.ChoiceField(choices = (GEEKS_CHOICES))
    
