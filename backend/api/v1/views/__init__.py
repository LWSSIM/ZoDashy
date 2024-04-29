#!/usr/bin/env python3
""" flask blueprint for api v1 views """


from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1/')

from backend.api.v1.views.status import *
from backend.api.v1.views.users import *
from backend.api.v1.views.companies import *
from backend.api.v1.views.departments import *
from backend.api.v1.views.employees import *
from backend.api.v1.views.attendances import *
