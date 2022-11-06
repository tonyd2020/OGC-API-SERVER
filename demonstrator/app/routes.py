from flask import render_template
from app import app
from app import db
from sqlalchemy import create_engine


@app.route('/')

@app.route('/index')
def index():
    db_string = "postgresql://sensorthings:ChangeMe@localhost:5432/sensorthings"
    db = create_engine(db_string)
    user = {'username': 'Brad'}

    result = db.execute("SELECT * FROM public.\"THINGS\";")


    return render_template('index.html', title='Home', user=user, result=result)