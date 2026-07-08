from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
# from .webforms import ProductForm, SearchForm, CategoryForm
# from .models import Products, Users, Categories
from mongoengine.errors import DoesNotExist, NotUniqueError, ValidationError
from bson import ObjectId
from datetime import datetime



root = Blueprint('root', __name__)


# DASHBOARD PAGE
@root.route('/dashboard')
@login_required
def dashboard():
    return render_template(
        'pages/dashboard.html'
    )