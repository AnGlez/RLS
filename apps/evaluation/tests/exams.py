# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from apps.evaluation.models import (
	Exam,
	Question,
	PossibleAnswer
)
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
import json
import os

__all__ = [
	'ExamTest'
]
User = get_user_model()


class ExamTest(TestCase):

	fixtures = [ 'users','concepts', 'courses', 'units']
	def setUp(self):
		self.client = Client(enforce_csrf_checks=False,HTTP_X_REQUESTED_WITH = 'XMLHttpRequest')
		self.user = User.objects.create_user(
			email_address = 'test1@example.com',
			username='test',
			password = 'asdfgh',
			is_staff= True
		)

	def test_add_question(self):

		self.client.login(username='test',password='asdfgh')

		exam = Exam.objects.create(
			name='test exam',
			unit=1,
			activated=True
		)
		response = self.client.post(reverse_lazy('preguntas:crear'), data = {
			'sentence': 'Pregunta prueba 1',
			'points': 5,
			'exam': 1,
			'answers':['opcion a','opcion b','opcion c'],
			'correct_answer':'opcion a'
			})
		ans = PossibleAnswer.objects.get(id = 1)
		quest = Question.objects.get(id=1)

		self.assertEqual(response.status_code,200)
		self.assertEqual(ans,quest.correct_answer)
		self.assertEqual(quest.exam,exam)

