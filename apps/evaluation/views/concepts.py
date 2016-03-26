from __future__ import unicode_literals
from django.shortcuts import redirect, render_to_response, RequestContext
from apps.evaluation.models import Concept,Course, Unit
from django.http import HttpResponseForbidden, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from apps.evaluation.decorators import ajax_required
from django.core.urlresolvers import reverse_lazy
from apps.evaluation.forms import QuestionForm
from django.views.generic import View
from django.http import JsonResponse
import json

__all__=[
	'create',
	'hierarchy'
]

class CreateConceptView(View):

	@method_decorator(login_required)
	@method_decorator(ajax_required)
	def post(self,request):

		concept = request.POST['name']
		if not Concept.objects.active().filter(name__iexact=concept).exists():
			c = Concept.objects.create(name=concept)
			return JsonResponse({
					'version': '1.0.0',
					'status': 201,
					'data': { 'name': c.name, 'id': c.id }
				}, status = 201)

	@method_decorator(login_required)
	@method_decorator(ajax_required)
	def get(self,request):
		c = request.GET['name']
		concepts = Concept.objects.active().filter(name__startswith=c)
		if len(concepts) > 0:
			return JsonResponse({
					'version': '1.0.0',
					'status': 201,
					'data': { 'concepts': c.name,}
				}, status = 201)

create = CreateConceptView.as_view()

class CreateHierarchyView(View):

	@method_decorator(login_required)
	def get(self,request,course_id):

		course = Course.objects.active().get(id=course_id)
		units = Unit.objects.active().filter(course=course)
		concepts = list()

		for u in units:
			concepts.extend(u.concepts.all())
		return render_to_response('concepts/hierarchy.html',context = RequestContext(request, locals()))

	@method_decorator(login_required)
	@method_decorator(ajax_required)
	def post(self, request, course_id):

		concepts = json.loads(request.POST['concepts'])

		for c in concepts:
			if c['related']:
				father = Concept.objects.active().get(id=c['id'])
				for r in c['related']:
					child = Concept.objects.active().get(id = r)
					child.required_by = father
					child.save()

			con = Concept.objects.get(id = c['id'])
			con.posX = c['posX']
			con.posY = c['posY']
			con.save()

		return JsonResponse({
					'version': '1.0.0',
					'status': 201,
				}, status = 201)

hierarchy = CreateHierarchyView.as_view()