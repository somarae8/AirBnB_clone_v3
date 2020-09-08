from flask import Flask
from models import storage
from api.v1.views import app_views
from flask import Blueprint
import * api.v1.views.index
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
