from django.contrib import admin
from .models import SubmitText, UserTxt, AnnotateCode
# Register your models here.
admin.site.register(SubmitText)
admin.site.register(UserTxt)
admin.site.register(AnnotateCode)
