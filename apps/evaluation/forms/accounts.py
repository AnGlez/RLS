# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.http import urlsafe_base64_encode as base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.shortcuts import RequestContext
from django.forms import *

__all__ = [ 'LoginForm' ]
User = get_user_model()

class LoginForm(Form):

	username = CharField(
		max_length = 255,
		required = True,
		widget = TextInput(attrs = { 'placeholder': _('Usuario') })
	)
	password = CharField(
		max_length = 128,
		required = True,
		widget = PasswordInput(attrs = { 'placeholder': _('Contraseña') })
	)

	def clean(self):

		username, password = self.cleaned_data['username'], self.cleaned_data['password']
		user = authenticate(username = username, password = password)

		if user is not None:

			if user.is_active: self.user = user
			else: raise ValidationError(_('El usuario no se encuentra activo en el sistema'))

		else: raise ValidationError(_('Correo electronico/contraseña erronea'))