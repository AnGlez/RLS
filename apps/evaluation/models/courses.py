# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.db.models import *
from _base import Model
from django.contrib.auth.models import User

class Course(Model):
	""" Course offered by instructor during a fixed period. Courses may only be offered once.
		Fields:
			-course name: official course name
			-course key:  unique key used to locate course, external use only
			-students: users enrolled in course
			-teacher: user teaching the course
	"""

	name = CharField(
		max_length = 64,
		verbose_name = _('nombre del curso')
	)
	code = CharField(
		verbose_name=_('clave del curso'),
		max_length=100
	)
	teacher = ForeignKey(User,
	                     related_name='profesor',
	                     verbose_name= 'profesor'

	)
	students = ManyToManyField(User,
	                           related_name='students',
	                           null = True,
	                           blank=True
	)
	def __str__(self):
		return self.name

	class Meta(object):

		verbose_name = _('curso')
		verbose_name_plural= _('cursos')
		app_label = 'evaluation'

class Unit(Model):
	""" Each one of the course's divisions; a unit is about one main concept,
		verbose_name = _('type name') topic.
		Fields:
			name: unit's name
			main_concept: unit's central topic (concept)
			course: the course related to current unit
	"""

	name = CharField(
		max_length=100,
		verbose_name=_('nombre de la unidad')
	)
	concepts = ManyToManyField('evaluation.Concept',
	                          related_name='concept',
	                          verbose_name=_('conceptos relacioandos')

	)
	course = ForeignKey('evaluation.Course',
	                    related_name='course',
	                    null= False,
	                    verbose_name=_('curso')
	)
	def __str__(self):
		return self.name

	class Meta(object):
		verbose_name = _('unidad')
		verbose_name_plural =_('unidades')
		app_label= 'evaluation'

