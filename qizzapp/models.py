from django.db import models

class Userlogin(models.Model):
    email=models.CharField(max_length=50)
    password=models.CharField(max_length=50,null=True, blank=True)
    quiz_mark=models.FloatField(default=0)
    time=models.DateTimeField(auto_now_add=True)
    section = models.ForeignKey('Statusbar', on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return f"{self.email} - {self.section.Name if self.section else 'No section'}"
    
class Statusbar(models.Model):
    Name=models.CharField(max_length=50)
    Des=models.CharField(max_length=50)
    Img=models.ImageField(upload_to='static/')
    def __str__(self):
        return self.Name
    
# ForeignKey is helps to links models
class Quizz(models.Model):
    Question=models.ForeignKey(Statusbar,on_delete=models.CASCADE,related_name='question')
    text=models.CharField(max_length=500)
    
    def __str__(self):
        return self.text
    
class Option(models.Model):
    quiz=models.ForeignKey(Quizz,on_delete=models.CASCADE,related_name='options')
    option_text=models.CharField(max_length=500) # we have create 4 options --> go to admin.py(code-line no: 4-9)
    is_correct=models.BooleanField(default=False)
    def __str__(self):
        return self.option_text
    
class Admin(models.Model):
    ad_email=models.CharField(max_length=50)
    username=models.CharField(max_length=50)
    ad_password=models.CharField(max_length=50)
    def __str__(self):
        return self.ad_email

# Create your models here.
