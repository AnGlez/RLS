# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.shortcuts import render_to_response, RequestContext
from apps.evaluation.models import Concept,Course, Unit, ChosenAnswer, Exam, Question
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from apps.evaluation.decorators import ajax_required
from django.core.validators import URLValidator
from django.http import HttpResponseForbidden
from django.views.generic import View
from django.http import JsonResponse
import json

__all__=[
	'create',
	'hierarchy',
	'resource',
	'resource_path'
]

class CreateConceptView(View):
	""" This view is in charge of creating the concepts involved in a unit via AJAX requests.
		When the user registers a unit, there is a text input where he can type the concepts name
		and hit enter to create them. This view is called every time the user writes a valid and unique
		concept name and hits enter.
	"""

	@method_decorator(login_required)
	@method_decorator(ajax_required)
	def post(self,request):
		"""
		The request contains the action the user took. If the user intends to add a concept,
		it will be checked that there is no other concept by that name. If not, the instance
		is created and a JSONResponse is sent so the template shows the recently created concept.
		If the action taken was delete, the view receives the concept id so it can be deleted.
		A JsonResponse is sent only to indicate the operation was successful
		:param request:
		:return JSONResponse:
		"""
		if request.POST['action'] == 'agregar':
			if not Concept.objects.active().filter(name = request.POST['name']).exists():
				concept = Concept.objects.create(name = request.POST['name'])
				return JsonResponse({
						'version': '1.0.0',
						'status': 201,
						'data': {'name': concept.name, 'id': concept.id}
					}, status = 201)
			else:
				return JsonResponse({
						'version': '1.0.0',
						'status': 401,
					}, status = 401)

		elif request.POST['action'] == 'borrar':
			concept = Concept.objects.get(id = request.POST['id'])
			concept.delete()
			return JsonResponse({
						'version': '1.0.0',
						'status': 201,
					}, status = 201)

create = CreateConceptView.as_view()

class AddResourceView(View):

	@method_decorator(ajax_required)
	def get(self,request):
		con = Concept.objects.get(id=request.GET["id"])
		if con.resource:
			return JsonResponse({
						'version': '1.0.0',
						'status': 201,
						'data': {'url': con.resource}
					}, status = 201)
		else:
			return JsonResponse({
						'version': '1.0.0',
						'status': 201,
						'data': {'url': "none"}
					}, status = 201)

	def post(self, request):

		validate = URLValidator()
		url = request.POST["resource"]
		try:
			validate(url)
			con = Concept.objects.get(id=request.POST['id'])
			con.resource = request.POST["resource"]
			con.save()

			return JsonResponse({
						'version': '1.0.0',
						'status': 201,
					}, status = 201)
		except:
			return JsonResponse({
						'version': '1.0.0',
						'status': 201,
					}, status = 400)

resource = AddResourceView.as_view()

class CreateHierarchyView(View):
	""" This view is in charge of creating a concept hierarchy by displaying a concept editor
		The user makes a relationship between each concept and submits the graph structure
		The hierarchy is made persistent for future use

	"""
	@method_decorator(login_required)
	def get(self,request,course_id):
		"""
		This method obtains a list of concepts related to every unit in the requested course
		and renders the template that shows them in the concept editor page
		:param request: HTTP GET request
		:param course_id: current course's id
		:return rendered template:
		"""
		if not request.user.is_staff:
			return HttpResponseForbidden()

		course = Course.objects.active().get(id=course_id)
		units = Unit.objects.active().filter(course=course)
		concepts = list()
		lines = []

		for u in units:
			concepts.extend(u.concepts.all())

		for c in concepts:
			related = c.prerequisite.all()
			for r in related:
				lines.append({'concept' : c.id, 'prerequisite':r.id})

		linesjson = json.dumps(lines)

		return render_to_response('concepts/hierarchy.html',context = RequestContext(request, locals()))

	@method_decorator(login_required)
	@method_decorator(ajax_required)
	def post(self, request, course_id):
		"""
		This method makes the hierarchy created by the user persistent.
		It receives a list of concepts, each concept contains its related concept's id
		Each related concept is stored in the concept's 'related' set
		:param request:
		:param course_id:
		:return:
		"""
		if not request.user.is_staff:
			return HttpResponseForbidden()

		concepts = json.loads(request.POST['concepts'])
		if concepts:
			for c in concepts:
				father = Concept.objects.get(id = c['id'])
				if c['related']:
					for r in c['related']:
						child = Concept.objects.active().get(id = r)
						father.required_by.add(child)

				father.posX = c['posX']
				father.posY = c['posY']
				father.save()

			return JsonResponse({
						'version': '1.0.0',
						'status': 201,
					}, status = 201)

		return render_to_response('concepts/hierarchy.html',context = RequestContext(request, locals()),status=401)

hierarchy = CreateHierarchyView.as_view()

class ViewResourcesView(View):

	def get(self, request, course_id):

		student = request.user
		course = Course.objects.get(id=course_id)
		chosen_answers = ChosenAnswer.objects.active().filter(student = student).all()
		missing_concepts = set()
		paths = []
		desc = []

		for c in chosen_answers: #agregar conceptos directamente incomprendidos
			if not c.answer.correct and c.question.exam.unit.course == course:
				missing_concepts.update(c.question.concepts.all())

		for i in missing_concepts: #cada camino inicia con un concepto directamente incomprendido
			desc.extend(i.required_by.all())
			i.children =[]
			for j in desc: # recorrido por amplitud
				if j in missing_concepts: desc.remove(j)
				for k in j.required_by.all():
					if k not in missing_concepts and k not in desc:
						desc.append(k)

				i.children.extend(desc)
			paths.append(i)
			desc[:] = []

		return render_to_response('results/resources.html', context=RequestContext(request, locals()), status=201)

resource_path = ViewResourcesView.as_view()
