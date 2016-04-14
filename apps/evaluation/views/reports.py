# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import redirect, render_to_response, RequestContext
from apps.evaluation.models import Exam, Unit, ChosenAnswer
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import View

__all__ = [
	'view'
]

class ViewReportView(View):

	@method_decorator(login_required)
	def get(self, request,unit_id):

		unit = Unit.objects.active().get(id = unit_id)
		if request.user.is_staff:
			pass
		else:
			exams = Exam.objects.active().filter(unit = unit)
			#results = ChosenAnswer.objects().filter(student = request.user, question = unit.exam)
		return render_to_response('courses/view-unit.html', context=RequestContext(request,locals()))



view = ViewReportView.as_view()


