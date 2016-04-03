# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import redirect, render_to_response, RequestContext
from apps.evaluation.models import Concept,Course, Unit
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from apps.evaluation.decorators import ajax_required
from django.http import HttpResponseForbidden
from django.views.generic import View
from django.http import JsonResponse
import json

__all__ = [
	'create'
]

class CreateUnitView(View):

	@method_decorator(login_required)
	def get(self, request,course_id):

		unit = Unit.objects.active().get(id = course_id)

		return render_to_response('courses/view-unit.html', context=RequestContext(request,locals()))

	@method_decorator(login_required)
	@method_decorator(ajax_required)

	def post(self, request,course_id):
		#TODO: validar

		course = Course.objects.active().get(id= course_id)
		name = request.POST['name']
		concept_ids = request.POST['concepts']

		unit = Unit(name = name, course = course)
		unit.save()
		for c in json.loads(concept_ids):
			unit.concepts.add(Concept.objects.active().get(id = c))

		unit.save()
		return JsonResponse({
						'version': '1.0.0',
						'status': 201,
						'data': {'name': unit.name, 'id': unit.id}
					}, status = 201)


create = CreateUnitView.as_view()


