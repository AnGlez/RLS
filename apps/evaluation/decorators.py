# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponseBadRequest

def ajax_required(view):
	""" AJAX request required decorator
		From <"https://djangosnippets.org/snippets/771/">
	@ajax_required
	def my_view(request):
	....
	"""

	def wrap(request, *args, **kwargs):

		if not request.is_ajax(): return HttpResponseBadRequest()
		return view(request, *args, **kwargs)

	wrap.__doc__ = view.__doc__
	wrap.__name__ = view.__name__

	return wrap