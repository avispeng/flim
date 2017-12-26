from flask import render_template, request, session, redirect, url_for
from app import webapp
import boto3
from boto3.dynamodb.conditions import Key, Attr
from decimal import Decimal

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

@webapp.route('/movies', methods=['GET'])
def movies_module():
    return


@webapp.route('/movies/new_item', methods=['GET','POST'])
def new_movie_item():
    """
    
    :return: 
    """
    if request.method == 'GET':
        return render_template('/movies/add_movie_item.html',title="Flim - Add One Movie Item")
    if request.method == 'POST':
        movie_title = request.form.get("movie_title")
        movie_no = request.form.get("movie_no")
        genres = []
        if 'genre' in request.form:
            genres = request.form.getlist("genre")
        else:
            genres = []
        if request.form.get("release_date", ""):
            release_date = request.form['release_date']
        else:
            release_date = " "

        # for inputs with multiple items, split them with commas and remove leading and trailing whitespaces
        directors = request.form.get("directors", "")
        if directors != "":
            directors = directors.split(",")
            for i in range(len(directors)):
                directors[i] = directors[i].strip()
        else:
            directors = []
        writers = request.form.get("writers", "")
        if writers != "":
            writers = writers.split(",")
            for i in range(len(writers)):
                writers[i] = writers[i].strip()
        else:
            writers = []
        stars = request.form.get("stars", "")
        if stars != "":
            stars = stars.split(",")
            for i in range(len(stars)):
                stars[i] = stars[i].strip()
        else:
            stars = []
        languages = request.form.get("languages", "")
        if languages != "":
            languages = languages.split(",")
            for i in range(len(languages)):
                languages[i] = languages[i].strip()
        else:
            languages = []
        countries = request.form.get("countries", "")
        if countries != "":
            countries = countries.split(",")
            for i in range(len(countries)):
                countries[i] = countries[i].strip()
        else:
            countries = []
        aka = request.form.get("aka", "")
        if aka != "":
            aka = aka.split(",")
            for i in range(len(aka)):
                aka[i] = aka[i].strip()
        else:
            aka = []

        rating = Decimal(0.)
        # connect to table
        table = dynamodb.Table('movies')
        # avoid repeating
        response = table.query(
            KeyConditionExpression=Key('movie_no').eq(movie_no)
        )
        error = False
        error_msg = ""
        if response['Count'] > 0:
            error = True
            error_msg = "Error: This movie already exists on Flim."
        if error:
            return render_template('/movies/add_movie_item.html', title="Flim - Add One Movie Item", msg_display=error_msg)

        # handling the poster
        fn = " "
        if 'poster' in request.files and request.files['poster'].filename:
            allowed_ext = {'jpg', 'jpeg', 'png', 'gif'}
            poster = request.files['poster']
            fn = poster.filename
            if '.' in fn and fn.rsplit('.', 1)[1].lower() in allowed_ext:
                fn = movie_no + '.' + fn.rsplit('.', 1)[1]
                # upload to S3
                s3 = boto3.resource('s3')
                bucket = s3.Bucket('flim-project')
                response = bucket.put_object(
                    ACL='public-read',
                    Body=poster,
                    Key='movies/'+fn
                )
            else:
                error = True
                error_msg = "Error: Invalid poster format. Please choose from jpg, jpeg, gif and png."
                if error:
                    return render_template('/movies/add_movie_item.html', title="Flim - Add One Movie Item",
                                           msg_display=error_msg)

        # add item to table
        response = table.put_item(
            Item={
                'movie_no': movie_no,
                'movie_title': movie_title,
                'rating': rating,
                'release data': release_date,
                'genres': genres,
                'movie_profile': {
                    'cast': {
                        'directors': directors,
                        'writers': writers,
                        'stars': stars,
                    },
                    'also known as': aka,
                    'language': languages,
                    'countries': countries,
                },
                'poster': fn
            }
        )
        msg_display = "Successfully add the movie to Flim."
        return render_template('/movies/add_movie_item.html', title="Flim - Add One Movie Item", msg_display=msg_display)


