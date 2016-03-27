from django.contrib.admin import site
from apps.evaluation.models import (
	Course,
	Unit,
	Exam,
	Question,
	Concept,
	PossibleAnswer,
	ChosenAnswer
)

site.register(Course)
site.register(Exam)
site.register(Unit)
site.register(Question)
site.register(Concept)
site.register(PossibleAnswer)
site.register(ChosenAnswer)
