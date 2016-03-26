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
	'create'
]

class AddQuestionView(View):

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
			if ans.text == request.POST['correct_answer']:
				ans.correct = True
			ans.save()

		return JsonResponse({
				'version': '1.0.0',
				'status': 201,
				'data': { 'sentence': q.sentence, 'id':q.id, 'points':q.points }
			}, status = 201)

create = AddQuestionView.as_view()

class EditQuestionView(View):

	@method_decorator(login_required)
	def get(self,request,question_id=0):
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
		#TODO: actualizar possible answers
		question = Question.objects.active().get(id=question_id)
		form = QuestionForm(request.POST,instance=question)
		if form.is_valid():
			question = form.instance
			form.save()
			mensaje = "La pregunta se actualizo correctamente"
			messages.add_message(request,messages.SUCCESS,mensaje)

			return redirect(reverse('examenes:view',kwargs={'exam_id': question.exam.id}))

edit = EditQuestionView.as_view()