from django.contrib import admin

# Register your models here.
from .models import Quiz, Question, Choice, Quiz_Answer, Question_Answer, User

admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Quiz_Answer)
admin.site.register(Question_Answer)
admin.site.register(User)

