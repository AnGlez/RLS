# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from model_utils.managers import InheritanceManager
from django.utils.encoding import smart_str
from django.db.models import *
from _base import Model, ActiveManager
from django.contrib.auth.models import User

class ChosenAnswer(Model):

	student = ForeignKey(User,related_name='student')
	answer = ForeignKey('evaluation.PossibleAnswer', related_name='chosen')
	question = ForeignKey('evaluation.Question', related_name='section', null=True)

	def __unicode__(self):
		return self.answer.text

	class Meta(object):
		verbose_name = 'respuesta'
		verbose_name_plural= 'respuestas'
		app_label='evaluation'

