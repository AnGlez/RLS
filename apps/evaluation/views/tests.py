# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.shortcuts import render_to_response, RequestContext
from apps.evaluation.models import ChosenAnswer, PossibleAnswer, Exam,Question
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from apps.evaluation.decorators import ajax_required
from django.views.generic import View
from django.http import JsonResponse
import json

__all__=[
	'answer',
	'results'
]

class AnswerTestView(View):
	""" This view handles the test submission performed by students.
		This view is called via AJAX requests, answers are received in JSON format and then stored in the database
	"""
	@method_decorator(login_required)
	@method_decorator(ajax_required)
	def post(self,request):

		ans = json.loads(request.POST['ans'])
		for a in ans:
			pa = PossibleAnswer.objects.active().get(id=a['a_id'])
			if not ChosenAnswer.objects.active().filter(question=pa.question, student = request.user).exists():
				ChosenAnswer.objects.create(student = request.user, question = pa.question, answer = pa)
			else:
				chosen = ChosenAnswer.objects.active().get(question = pa.question, student = request.user)
				chosen.answer = pa
				chosen.save()

		return JsonResponse({
					'version': '1.0.0',
					'status': 201,
				}, status = 201)

answer = AnswerTestView.as_view()

class ViewResultsView(View):

	@method_decorator(login_required)
	def get(self,request,exam_id):

		test = Exam.objects.active().get(id = exam_id)
		questions = Question.objects.active().filter(exam =test)
		concepts = set()
		missing_concepts = []
		for q in questions:
			q.ans = ChosenAnswer.objects.active().filter(question = q, student=request.user)
			correct =  len(q.ans) > 0 and q.ans[0].answer.correct
			concepts.update(q.concepts.all())
			if not correct:
				q.correct = PossibleAnswer.objects.filter(question = q, correct = True)
				missing_concepts.extend(q.concepts.all())
		count = len(concepts) - len(missing_concepts)
		if len(concepts) > 0 : percentage = count * 100 / len(concepts)
		else : percentage = 0
		return render_to_response('results/exam_results.html',context=RequestContext(request,locals()))

results = ViewResultsView.as_view()