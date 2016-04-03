# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from model_utils.managers import InheritanceManager
from django.utils.encoding import smart_str
from django.db.models import *
from _base import Model, ActiveManager
from django.contrib.auth.models import User

