# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import (
	AbstractBaseUser,
	Permission,
	BaseUserManager,
	PermissionsMixin
)
from django.utils.translation import ugettext_lazy as _
from django.utils.functional import cached_property
from django.utils.timezone import now
from django.conf import settings
from django.db.models import *
from _base import Model, ActiveManager

class UserManager(ActiveManager, BaseUserManager):

	def _create(self, email_address = None, password = None, **kwargs):

		if email_address is None: raise ValueError('Email address cannot be null')

		email = UserManager.normalize_email(email_address)
		user = self.model(
			email_address = email,
			date_joined = now(),
			**kwargs
		)
		user.set_password(password)
		user.save()

		return user
	def create_user(self, email_address, password = None, **extra_fields):
		return self._create(email_address, password, **extra_fields)
	def create_superuser(self, email_address, password, **extra_fields):
		return  self._create(email_address, password, is_superuser = True, **extra_fields)

class User(Model, AbstractBaseUser, PermissionsMixin):

	email_address = EmailField(
		max_length = 255,
		null = False,
		blank = False,
		unique = True,
		verbose_name = _('email')
	)
	name = CharField(
		max_length = 100,
		null = False,
		blank = False,
		verbose_name = _('nombre')
	)

	role = ForeignKey('apps.evaluation.Role',
		related_name = 'members',
		null = True,
		default = None,
	    verbose_name = _('rol')
	)

	objects = UserManager()
	USERNAME_FIELD = 'email_address'
	REQUIRED_FIELDS = [
		'password',
		'first_name'
	]

	@property
	def is_active(self): return self.active
	@property
	def is_staff(self): return self.belongs_to(name = 'user manager')

	def belongs_to(self, name = '', **kwargs):

		def _belongs_recursive(role, target):

			if role is None: return False

			if role.id == target.id: return True
			return _belongs_recursive(role.base, target)

		target = Role.objects.active().get(name = name, **kwargs)
		return _belongs_recursive(self.role, target)


	class Meta(object):

		verbose_name = _('usuario')
		verbose_name_plural = _('usuarios')
		app_label = 'evaluation'

class Role(Model):

	name = CharField(
		max_length = 64,
		null = False,
		blank = False,
		verbose_name = _('rol')
	)
	base = ForeignKey('self',
		related_name = 'subroles',
		null = True,
	    verbose_name = _('rol base')
	)
	base_permissions = ManyToManyField(Permission,
		related_name = 'roles',
		related_query_name = 'role',
		verbose_name = _('permisos')
	)

	@cached_property
	def permissions(self):

		query = self._get_permissions_query()
		return Permission.objects.filter(query)

	def _get_permissions_query(self, query = None):

		if query is None: query = Q(role__id = self.id)
		query = (query | self.role._get_permissions_query(query = query))

		return query

	def __str__(self): return self.name

	class Meta(object):

		verbose_name = _('rol')
		verbose_name_plural = _('roles')
		app_label = 'evaluation'