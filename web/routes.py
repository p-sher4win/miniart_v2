from flask import Blueprint, render_template, request, flash, redirect, url_for
# from .models import Products, Feedback, Categories, Review
# from .webforms import FeedbackForm, ReviewForm
from mongoengine.errors import DoesNotExist
from bson import ObjectId
import random
from datetime import datetime



routes = Blueprint('routes', __name__)


# HOME PAGE
@routes.route('/')
def home():
    return render_template(
        'pages/home.html'
    )