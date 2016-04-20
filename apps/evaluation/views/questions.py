# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from apps.evaluation.models import Question, PossibleAnswer, Exam, Unit,Concept
from django.shortcuts import redirect, render_to_response, RequestContext
from django.http import HttpResponseForbidden, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from apps.evaluation.decorators import ajax_required
from apps.evaluation.forms import QuestionForm
from django.core.urlresolvers import reverse
from django.views.generic import View
from django.http import JsonResponse
from django.contrib import messages

__all__=[
	'create',
	'edit'
]

class AddQuestionView(View):

	""" This view handles question registry via ajax requests

	"""
	@method_decorator(login_required)
	@method_decorator(ajax_required)
	def get(self,request):
		exam = Exam.objects.get(id =request.GET['exam'])
		questions = Question.objects.active().filter(exam=exam)
		concepts = exam.unit.concepts.all()
		return JsonResponse({
				'version': '1.0.0',
				'status': 201,
				'data': { 'questions': questions }
			}, status = 201)


	@method_decorator(login_required)
	@method_decorator(ajax_required)
	@method_decorator(csrf_protect)
	def post(self,request):
		""" This makes the exam persistent as well as its options
		:param request:
		:return JsonResponse:
		"""
		ex = Exam.objects.active().get(id=request.POST['exam'])

		q = Question(
			sentence = request.POST['sentence'],
			exam = ex
		)
		q.save()
		concepts = request.POST.getlist('concepts[]')

		for c in concepts:
			con = Concept.objects.get(id=c)
			q.concepts.add(con)
		q.save()
		answers = request.POST.getlist('answers[]')
		for a in answers:
			ans = PossibleAnswer(
				text = a,
				question = q
			)
			if ans.text == request.POST['correct_answer']:
				ans.correct = True
			ans.save()

		return JsonResponse({
				'version': '1.0.0',
				'status': 201,
				'data': { 'sentence': q.sentence, 'id':q.id}
			}, status = 201)

create = AddQuestionView.as_view()

class EditQuestionView(View):
	""" This view handles question edition as well as possible answer edition.
	"""
	@method_decorator(login_required)
	def get(self,request,question_id=0):
		"""
		Renders question form with its possible answers so they can be updated too
		:param request:
		:param question_id:
		:return:
		"""
		if not request.user.is_staff:
			return HttpResponseForbidden()

		try: question = Question.objects.active().get(id=question_id)
		except Question.DoesNotExist:
			return HttpResponseForbidden()
		else:
			question_form = QuestionForm(instance=question)
			question_form.fields['concepts'].queryset = question.exam.unit.concepts.all()
			answers = PossibleAnswer.objects.active().filter(question=question)
			return render_to_response('questions/edit.html',context = RequestContext(request, locals()))

	@method_decorator(login_required)
	def post(self,request,question_id=0):
		"""
		This validates and makes the changes done by the user persistent and then renders the Exam view page
		:param request:
		:param question_id:
		:return rendered template:
		"""
		question = Question.objects.active().get(id=question_id)
		question_form = QuestionForm(request.POST,instance=question)
		if question_form.is_valid():
			question = question_form.instance
			question_form.save()
			mensaje = "La pregunta se actualizó correctamente"
			messages.add_message(request,messages.SUCCESS,mensaje)
			return redirect(reverse('examenes:view',kwargs={'exam_id': question.exam.id}))

		messages.add_message(request, messages.ERROR, 'Favor de llenar todos los campos')
		question_form.fields['concepts'].queryset = question.exam.unit.concepts.all()
		answers = PossibleAnswer.objects.active().filter(question=question)
		return render_to_response('questions/edit.html',context = RequestContext(request, locals()),status=401)

edit = EditQuestionView.as_view()