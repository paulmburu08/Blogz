from flask_login import login_required
from flask import render_template
from . import main

@main.route('/')
@login_required
def index():

    title = 'BLOGZ'

    return render_template('index.html', title = title)