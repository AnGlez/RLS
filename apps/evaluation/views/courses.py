# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from apps.evaluation.models import Course, Unit, Exam, ChosenAnswer
from django.shortcuts import render_to_response, RequestContext
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from apps.evaluation.decorators import ajax_required
from django.contrib.auth.models import User
from django.views.generic import View
from django.http import JsonResponse
import json

__all__=[
	'create',
	'view',
	'list'
]

class ListCourseView(View):

	@method_decorator(login_required)
	def get(self,request):
		if request.user.is_staff:
			courses = Course.objects.active().filter(teacher=request.user)
		else:
			courses = Course.objects.active().filter(students=request.user)

		return render_to_response('courses/list.html',context = RequestContext(request, locals()))

list = ListCourseView.as_view()

class ViewCourseView(View):

	@method_decorator(login_required)
	def get(self, request, course_id):

		course = Course.objects.active().get(id=course_id)
		units = Unit.objects.active().filter(course=course)
		exams = []
		for u in units:
				exams.extend(Exam.objects.active().filter(unit= u).all())

		if request.user.is_staff:
			students = course.students.all()
			users = User.objects.exclude(id__in=students.values('id'))
			return render_to_response('courses/detail.html', context=RequestContext(request, locals()))
		else:
			for e in exams:
				if len(ChosenAnswer.objects.active().filter(question__exam = e, student = request.user)) > 0:
					e.completed = True
				else:
					e.completed = False
			return render_to_response('courses/detail-student.html', context=RequestContext(request, locals()))



	@method_decorator(login_required)
	@method_decorator(ajax_required)
	def post(self,request,course_id):

		course = Course.objects.active().get(id=course_id)
		action = request.POST['action']

		if action == 'borrar':
			student = User.objects.all().get(id=request.POST['user_ids'])
			course.students.remove(student)

			return JsonResponse({
					'version': '1.0.0',
					'status': 201,
				}, status = 201)

		elif action == 'guardar':
			ids = json.loads(request.POST['user_ids'])
			students = []
			for i in ids:
				s = User.objects.all().get(id = i)
				course.students.add(s)
				students.append({'id': s.id, 'username': s.username, 'first_name':s.first_name, 'last_name':s.last_name})

			return JsonResponse({
					'version': '1.0.0',
					'status': 201,
					'data': {'students': json.dumps(students)}
				}, status = 201)

view = ViewCourseView.as_view()