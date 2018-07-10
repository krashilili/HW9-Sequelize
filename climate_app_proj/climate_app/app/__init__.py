from flask import Blueprint

app = Blueprint('/test',__name__,)

from . import views
