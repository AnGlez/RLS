# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.shortcuts import redirect, render_to_response, RequestContext
from apps.evaluation.models import Exam,Unit,Question,PossibleAnswer, ChosenAnswer
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse_lazy, reverse
from apps.evaluation.forms import ExamForm, QuestionForm
from django.http import HttpResponseForbidden
from django.views.generic import View
from django.db.models import Q
from django.contrib import messages

__all__ = [
	'create',
	'edit',
	'view',
	'list'
]

class CreateExamView(View):
	"""	Class in charge of creating exams for courses
	"""
	@method_decorator(login_required)
	def get(self,request):
		"""
		Renders the exam form and obtains active units to populate the form
		:param request:
		:return:
		"""
		if not request.user.is_staff:
			return HttpResponseForbidden()
		form = ExamForm()
		unit = Unit.objects.active()
		return render_to_response('exams/create.html', context = RequestContext(request, locals()))


	@method_decorator(login_required)
	def post(self,request):
		"""
		Validates and saves exam instance
		:param request:
		:return rendered template:
		"""
		if not request.user.is_staff:
			return HttpResponseForbidden()

		form = ExamForm(request.POST)

		if form.is_valid():
			exam = form.instance
			form.save()
			mensaje = "El examen '"+exam.name+"' fue agregado exitosamente"
			messages.add_message(request,messages.SUCCESS,mensaje)
			return redirect(reverse_lazy('examenes:listar'))

		mensaje = "Favor de llenar todos los campos"
		messages.add_message(request,messages.ERROR,mensaje)
		return render_to_response('exams/create.html',
			context = RequestContext(request, locals()),
			status = 401
		)

create = CreateExamView.as_view()

class ListExamsView(View):
	""" This view renders the list of exams available
	"""
	#TODO: Filtrar examenes por profesor

	@method_decorator(login_required)
	def get(self,request):
		if request.user.is_staff:
			exams = Exam.objects.active().filter(unit__course__teacher = request.user)
		else:
			exams = Exam.objects.active().filter(Q(unit__course__students=request.user))
			for e in exams:
				if len(ChosenAnswer.objects.active().filter(question__exam = e, student = request.user)) > 0:
					e.completed = True
				else:
					e.completed = False
					if not e.activated: exams.exclude(id = e.id)

		return render_to_response('exams/list.html',context=RequestContext(request,locals()))


list = ListExamsView.as_view()

class ViewExamView(View):

	@method_decorator(login_required)
	def get(self,request,exam_id=0):

		try: exam = Exam.objects.active().get(id=exam_id)
		except Exam.DoesNotExist:
			return HttpResponseForbidden()
		else:
			preguntas = Question.objects.active().filter(exam=exam)
			for p in preguntas:
					p.answers = PossibleAnswer.objects.active().filter(question=p)
					p.num_answers = len(p.answers)
			if request.user.is_staff:
				question_form = QuestionForm()
				return render_to_response('exams/detail.html',context = RequestContext(request, locals()))
			else:
				time = int(exam.duration.hour) * 3600 + int(exam.duration.minute) * 60 + int(exam.duration.second)
				return render_to_response('exams/student_test.html',context = RequestContext(request, locals()))


view = ViewExamView.as_view()

class EditExamView(View):

	@method_decorator(login_required)
	def get(self,request,exam_id=0):
		if not request.user.is_staff:
			return HttpResponseForbidden()

		try: exam = Exam.objects.active().get(id=exam_id)
		except Exam.DoesNotExist:
			return HttpResponseForbidden()
		else:
			if request.user.is_staff:
				form = ExamForm(instance=exam)
				question_form = QuestionForm()
				question_form.fields['concepts'].queryset = exam.unit.concepts.all()
				preguntas = Question.objects.active().filter(exam=exam)
				for p in preguntas:
					p.answers = PossibleAnswer.objects.active().filter(question=p)
					p.num_answers = len(p.answers)
				return render_to_response('exams/edit.html',context = RequestContext(request, locals()))
			else:
				return HttpResponseForbidden()

	@method_decorator(login_required)
	def post(self,request,exam_id=0):

		if not request.user.is_staff:
			return HttpResponseForbidden()

		exam = Exam.objects.active().get(id=exam_id)
		form = ExamForm(request.POST, instance=exam)

		if form.is_valid():
			exam = form.instance
			form.save()
			mensaje = "El examen se actualizó correctamente"
			messages.add_message(request,messages.SUCCESS,mensaje)
			return redirect(reverse('examenes:view',kwargs={'exam_id': exam.id}))

		mensaje = "Favor de llenar todos los campos"
		messages.add_message(request,messages.ERROR,mensaje)
		return render_to_response('exams/edit.html',context = RequestContext(request, locals()),status=401)

edit = EditExamView.as_view()