# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from model_utils.managers import InheritanceManager
from django.utils.encoding import smart_str
from django.db.models import *
from _base import Model, ActiveManager
from django.contrib.auth.models import User

class Exam(Model):
	""" Representation of a unit's exam. An exam cannot be updated if it has already been answered by a student.
		Fields:
			- instructions: text containing special directions for students
			- unit: fk to the unit it evaluates
			- questions: set of questions
	"""
	name = CharField(
		max_length=60
	)
	instructions = CharField(
		max_length=400,
		blank=True
	)
	unit = ForeignKey('evaluation.Unit',
	                  related_name= 'unit',
	                  null= False,
	                  blank=False
	)
	activated = BooleanField(default=False)
	duration = TimeField(null=True)

	def __unicode__(self):
		return self.name

	class Meta(object):
		verbose_name=_('examen')
		verbose_name_plural= _('exámenes')
		app_label = 'evaluation'

class Question(Model):
	""" Question that will be evaluated in an exam. A question may be present in more than one exam.
		Fields:
			- sentence: question description
			- type: whether it's multiple choice, multiple with more than one correct answer or open
			- concepts: concepts being evaluated in such question
			- correct_answer: if it's not an open question, reference to the expected answer
			-points: question's value if it is answered correctly

	"""

	sentence = TextField(blank=False)

	concepts = ManyToManyField('evaluation.Concept',
	                           related_name='related_concepts',
	                           blank=True,
	                           null=True
	)

	points = PositiveSmallIntegerField(blank = False)

	exam = ForeignKey('evaluation.Exam',
	                  related_name='exam',
	                  null = True
	                  )

	def __unicode__(self):
		return self.sentence

	class Meta(object):
		verbose_name=_('pregunta')
		verbose_name_plural = _('preguntas')
		app_label = 'evaluation'

class Concept(Model):
	""" Concept being evaluated per question or unit. A concept's prerequisite is the knowledge needed to understand it.
		If the prerequisite is marked as a misconception, the present concept will also be considered a misconception.
		Fields:
			- name: concept's title
			- prerequisite: predecessor concept
	"""
	name = CharField(
		blank= False,
		max_length= 200,

	)
	required_by = ManyToManyField('evaluation.Concept',
		                         related_name='prerequisite',
	                         blank= True,
	                         null = True
	)
	posX = FloatField(blank=True, null=True)
	posY = FloatField(blank=True, null=True)

	def __unicode__(self):
		return self.name

	class Meta(object):
		verbose_name= _('concepto')
		verbose_name_plural = _('conceptos')
		app_label = 'evaluation'

class PossibleAnswer(Model):
	""" Possible answers for multiple choice questions. Fields:
		-Text
		-Question
	"""
	text = TextField(
		max_length=500,
		blank= False
	)
	question = ForeignKey('evaluation.Question',
	                      related_name='question',
	                      null=True
	                      )
	correct = BooleanField(default=False)

	def __unicode__(self):
		return self.text

	class Meta(object):
		verbose_name = _('opción')
		verbose_name_plural = _('opciones')
		app_label = 'evaluation'