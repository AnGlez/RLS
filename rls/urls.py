from __future__ import unicode_literals
from django.shortcuts import render_to_response, RequestContext
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView
from django.conf.urls import include, url
from django.http import HttpResponse
from apps.evaluation import views
from django.contrib import admin


redirect = RedirectView.as_view


urlpatterns = [
	url(r'^grappelli/', include('grappelli.urls')), # grappelli URLS
	url(r'^admin/', include(admin.site.urls)), # admin site

	url(r'^$',views.courses.list, name='home'),
	#Login and logout
	url(r'^accounts/',include([
		url(r'^login/$', views.accounts.login, name = 'login'),
		url(r'^logout/$', views.accounts.logout, name = 'logout')],namespace="accounts")),

	#Exam management
	url(r'^examenes/',include([

		url(r'crear/$',views.exams.create,name='crear'), #get, post
		url(r'^$',views.exams.list,name='listar'),
		url(r'^responder',views.tests.answer, name='responder'),
		url(r'^(?P<exam_id>[\d]+)/', include([

	 		url(r'^$',  views.exams.view, name = 'view'), #get, post
			url(r'^editar', views.exams.edit, name='edit'),
			url(r'^resultados',views.tests.results, name = 'results')

		]))], namespace="examenes")),

	#Question management
	url(r'^preguntas/',include([

		url(r'crear/$',views.questions.create,name='crear'), #get, post
		url(r'^(?P<question_id>[\d]+)/editar/$',views.questions.edit,name='edit') #get,post
	],namespace="preguntas")),

	#Concept management
	url(r'^conceptos/',include([
		url(r'crear/$',views.concepts.create, name="crear"), #get, post
		url(r'^(?P<course_id>[\d]+)/editor/$',views.concepts.hierarchy,name="ordenar") #get, post
		],namespace="conceptos")),

	#Course management
	url(r'^cursos/',include([
		#url(r'crear/$',views.concepts.create, name="crear"), #get, post
		url(r'^$',views.courses.list,name="listar"), #get, post
		url(r'^(?P<course_id>[\d]+)/', include([
			url(r'^$',views.courses.view, name='view')
		]))],namespace="cursos")),

	# Unir management
	url(r'^unidades/',include([
		url(r'(?P<course_id>[\d]+)/', include([
			url(r'crear/$',views.units.create, name="create"),
		])), #get, post
		url(r'(?P<unit_id>[\d]+)/', include([
			url(r'^$', views.reports.view, name="view")
		]))
		],namespace="unidades")),

 ]