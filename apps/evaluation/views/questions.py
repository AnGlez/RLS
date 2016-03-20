from __future__ import unicode_literals
from django.shortcuts import redirect, render_to_response, RequestContext
from apps.evaluation.models import Question,Concept, PossibleAnswer, Exam
from django.http import HttpResponseForbidden, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from apps.evaluation.decorators import ajax_required
from django.core.urlresolvers import reverse_lazy
from apps.evaluation.forms import QuestionForm
from django.http import JsonResponse
from django.views.generic import View
__all__=[
	'create'
]

class AddQuestionView(View):

	@method_decorator(login_required)
	@method_decorator(ajax_required)
	def get(self,request):
		exam = Exam.objects.get(id =request.GET['exam'])
		questions = Question.objects.active().filter(exam=exam)

		return JsonResponse({
				'version': '1.0.0',
				'status': 201,
				'data': { 'questions': questions }
			}, status = 201)

	def validate(self, data, ex):
		errores = []
		if data['sentence'] is None: errores.append('La pregunta no puede ser nula')
		if data['points'] < 0 : errores.append('Las preguntas no deben tener puntaje negativo')
		if Question.objects.active().filter(sentence__iexact = data['sentence'], exam=ex).exists():
			errores.append('Ya existe esta pregunta en el examen')

		return errores

	@method_decorator(login_required)
	@method_decorator(ajax_required)
	@method_decorator(csrf_protect)
	def post(self,request):
		#TODO: Validar que las respuestas no sean nulas, que haya una respuesta correcta, que las respuestas no se repitan

		ex = Exam.objects.active().get(id=request.POST['exam'])
		errores = self.validate(request.POST,ex)
		print errores
		q = Question(
			sentence = request.POST['sentence'],
			points = request.POST['points'],
			exam = ex
		)
		q.save()
		answers = request.POST.getlist('answers[]')
		for a in answers:
			ans = PossibleAnswer(
				text = a,
				question = q
			)
			ans.save()
			if ans.text == request.POST['correct_answer']:
				ans.correct = True

		return JsonResponse({
				'version': '1.0.0',
				'status': 201,
				'data': { 'sentence': q.sentence }
			}, status = 201)

create = AddQuestionView.as_view()