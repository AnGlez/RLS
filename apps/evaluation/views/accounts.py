# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth import (
	login as login_to_site,
	logout as logout_from_site,
	update_session_auth_hash as update_session
)
from django.shortcuts import render_to_response, redirect, RequestContext
from django.contrib.auth.tokens import default_token_generator as tokens
from django.utils.http import urlsafe_base64_decode as base64_decode
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import update_last_login
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from apps.evaluation.forms import LoginForm
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import get_user_model
from django.http import HttpResponseForbidden
from django.utils.http import force_text
from django.views.generic import View

__all__ = [
	'login',
	'logout',
]

class LoginView(View):
	""" This view is in charge of authenticating users into the system and storing their data in a session
		The authentication determines the user's role
	"""
	def get(self,request):
		# Get redirect URL
		redirect_url = request.REQUEST.get('next', reverse_lazy('cursos:listar'))

		# Check if user has been authenticated before - if so, redirect him/her to the main site
		if request.user is not None and request.user.is_authenticated():
			return redirect(redirect_url)

		# Create the login form and render the template
		form = LoginForm()
		return render_to_response('accounts/login.html', context = RequestContext(request, locals()))

	@method_decorator(csrf_protect)
	def post(self, request):

		# Get redirect URL
		redirect_url = request.REQUEST.get('next', reverse_lazy('cursos:listar'))

		# Check if user has been authenticated before - if so, redirect him/her to the main site
		if request.user is not None and request.user.is_authenticated():

			return redirect(redirect_url)

		form = LoginForm(request.POST)
		if form.is_valid():

			# Login the authenticated user to the site and redirect - remember to log this event
			user = form.user
			login_to_site(request, user)
			update_last_login(None, user = user)

			return redirect(redirect_url)

		# Login failed - report errors back to the user

		return render_to_response('accounts/login.html',
			context = RequestContext(request, locals()),
			status = 401
		)
login = LoginView.as_view()

class LogoutView(View):
	"""
		This view is in charge of destroying session variables when the user is finished using the system
	"""
	@method_decorator(login_required)
	def get(self, request):

		# log out the user
		logout_from_site(request)
		return redirect(reverse_lazy('accounts:login'))

logout = LogoutView.as_view()

