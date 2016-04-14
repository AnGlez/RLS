# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from django.forms import *
from django.forms import ModelForm as Form
from django_select2.forms import Select2MultipleWidget
from apps.evaluation.models import Exam, Question

__all__ = [ 'ExamForm','QuestionForm']

class ExamForm(Form):
		class Meta(object):
			model = Exam
			fields = [
				'name',
				'unit',
				'activated',
				'instructions',
				'duration'
			]
			widgets = {
				'name': TextInput(attrs = { 'placeholder': _('Título del examen'),'class':'form-control' }),
				'instructions': Textarea(attrs = { 'placeholder': _('Indicaciones del examen'), 'rows': 6, 'class':'form-control' }),
				'unit':Select(attrs={'class':'form-control'}),
				'activated': CheckboxInput(),
				'duration': TextInput(attrs={'class':'form-control floating-label', 'id':'time'})
			}
class QuestionForm(Form):
	class Meta(object):
		model = Question
		fields = [
			'sentence',
			'concepts',
		]
		widgets = {
			'sentence':TextInput(attrs={'placeholder':'Escribe el enunciado de la pregunta','class':'form-control','required':'required'}),
			'concepts':Select2MultipleWidget(attrs={'id':'concept-select','style':'width:100%','required':'required','placeholder':'Escribe un concepto'}),
		}