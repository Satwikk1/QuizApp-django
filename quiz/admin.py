from django.contrib import admin
from . import models

# Register your models here.



class AnswersInline(admin.TabularInline):
	model=models.Answer

class QuestionAdmin(admin.ModelAdmin):
	inlines=[AnswersInline]

class QuizModelDisplayFields(admin.ModelAdmin):
	readonly_fields = ('id',)

admin.site.register(models.Question, QuestionAdmin)
admin.site.register(models.Answer)
admin.site.register(models.Quiz, QuizModelDisplayFields)
