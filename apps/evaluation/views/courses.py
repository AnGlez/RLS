from __future__ import unicode_literals
from apps.evaluation.models import Course
from django.shortcuts import redirect, render_to_response, RequestContext
from django.http import HttpResponseForbidden, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from apps.evaluation.decorators import ajax_required
from django.core.urlresolvers import reverse
from django.views.generic import View
from django.http import JsonResponse
from django.contrib import messages

__all__=[
	'create',
	'view'
]

class ListCourseView(View):

	@method_decorator(login_required)
	def get(self,request):

		courses = Course.objects.active().filter(teacher=request.user)
		return render_to_response('courses/list.html',context = RequestContext(request, locals()))

list = ListCourseView.as_view()