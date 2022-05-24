from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.
from django.forms import ModelForm, TextInput, Textarea


class Setting(models.Model):
    objects = None
    STATUS = (
        ('True', 'Yes'),
        ('False', 'No'),
    )

    title = models.CharField(max_length=150)
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=200)
    company = models.CharField(max_length=60)
    adress = models.CharField(blank=True, max_length=150)
    phone = models.CharField(blank=True, max_length=20)
    fax = models.CharField(blank=True, max_length=20)
    email = models.CharField(blank=True, max_length=60)
    smtpserver = models.CharField(blank=True, max_length=30)
    smtpemail = models.CharField(blank=True, max_length=30)
    smtppassword = models.CharField(blank=True, max_length=10)
    smtpport = models.CharField(blank=True, max_length=150)
    icon = models.ImageField(blank=True, upload_to='images/')
    facebook = models.CharField(blank=True, max_length=60)
    instagram = models.CharField(blank=True, max_length=60)
    twitter = models.CharField(blank=True, max_length=60)
    aboutus: RichTextUploadingField = RichTextUploadingField(blank=True)
    contact = RichTextUploadingField(blank=True)
    references = RichTextUploadingField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class ContactFormMessage(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Read', 'Read'),
        ('Closed', 'Closed'),
    )
    name = models.CharField(blank=True, max_length=35)
    email = models.CharField(blank=True, max_length=60)
    subject = models.CharField(blank=True, max_length=60)
    message = models.CharField(blank=True, max_length=300)
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    ip = models.CharField(blank=True, max_length=25)
    note = models.CharField(blank=True, max_length=170)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ContactForm(ModelForm):
    class Meta:
        model = ContactFormMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': TextInput(attrs={'class': 'input', 'placeholder': 'Name & Surname'}),
            'subject': TextInput(attrs={'class': 'input', 'placeholder': 'Subject'}),
            'email': TextInput(attrs={'class': 'input', 'placeholder': 'Email Address'}),
            'message': Textarea(attrs={'class': 'input', 'placeholder': 'Your Message', 'rows': '5'}),
        }


class FAQ(models.Model):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )
    ordernumber = models.IntegerField()
    question = models.CharField(max_length=250)
    answer = RichTextUploadingField()
    status = models.CharField(max_length=10, choices=STATUS)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question
