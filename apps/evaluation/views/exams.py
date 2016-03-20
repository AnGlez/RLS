from __future__ import unicode_literals
from django.shortcuts import redirect, render_to_response, RequestContext
from django.http import HttpResponseForbidden, HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse_lazy
from apps.evaluation.models import Exam,Unit,Question
from django.contrib.auth.models import User
from apps.evaluation.forms import ExamForm, QuestionForm
from django.views.generic import View


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
		if not request.user.is_staff:
			return HttpResponseForbidden()

		form = ExamForm()
		unit = Unit.objects.active()
		return render_to_response('exams/create.html', context = RequestContext(request, locals()))


	@method_decorator(login_required)
	def post(self,request):

		form = ExamForm(request.POST)

		if form.is_valid():
			exam = form.instance
			form.save()
			return redirect(reverse_lazy('examenes:listar'))

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

		exams = Exam.objects.active().filter()
		return render_to_response('exams/list.html',context=RequestContext(request,locals()))


list = ListExamsView.as_view()

class ViewExamView(View):

	@method_decorator(login_required)
	def get(self,request,exam_id=0):
		try: exam = Exam.objects.active().get(id=exam_id)
		except Exam.DoesNotExist:
			return HttpResponseForbidden()
		else:
			if request.user.is_staff:
				form = ExamForm(instance=exam,initial = { 'user': request.user })
				question_form = QuestionForm()
				preguntas = Question.objects.active().filter(exam=exam)
				return render_to_response('exams/detail.html',context = RequestContext(request, locals()))
			else:
				return render_to_response('exams/student_test.html',context = RequestContext(request, locals()))



	@method_decorator(login_required)
	def post(self,request,exam_id=0):

		exam = Exam.objects.active().get(id=exam_id)
		form = ExamForm(request.POST, instance=exam, initial={ 'user': request.user })

		if form.is_valid():
			exam = form.instance
			form.save()
			mensaje = 'El examen se actualizo correctamente'
			return render_to_response('exams/detail.html',context = RequestContext(request, locals()),status=401)

		return render_to_response('exams/detail.html',context = RequestContext(request, locals()),status=401)

view = ViewExamView.as_view()

