from flask import render_template, request, session, redirect, url_for
from app import webapp
import hashlib
import random
import boto3
from boto3.dynamodb.conditions import Key
from app import movies
from app import tests
from app import users


dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

@webapp.route('/')
def main():
    """
    
    :return: 
    """
    return render_template("main.html",title="Flim", login_block=None)


@webapp.route('/register', methods=['GET'])
def signup_get():
    """
    
    :return: 
    """
    return render_template("register.html", title="Flim - Signup")


@webapp.route('/register_submit', methods=['POST'])
def signup_submit():
    """
    
    :return: 
    """
    username = request.form.get('username')
    pwd = request.form.get('password')

    # check length of input
    error = False
    error_msg = ""
    if len(username) < 6 or len(username) > 20 or len(pwd) < 6 or len(pwd) > 20:
        error = True
        error_msg = "Error: Both username and password should have length of 6 to 20!"
    if error:
        return render_template("register.html", title="Flim - Signup", signup_error_msg=error_msg,
                               sign_username=username)

    alphanum = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    # check if the username is valid
    for char in username:
        if char not in alphanum:
            error = True
            error_msg = "Error: Username must be combination of characters or numbers!"
        if error:
            return render_template("register.html", title="Flim - Signup", signup_error_msg=error_msg,
                                   sign_username=username)
    # connect to database
    table = dynamodb.Table('users')
    # check whether username already exists in users table
    response = table.query(
        KeyConditionExpression=Key('username').eq(username)
    )
    if response['Count'] != 0:
        error = True
        error_msg = "Error: Username already exists!"
    if error:
        return render_template("register.html", title="Flim - Signup", signup_error_msg=error_msg,
                               sign_username=username)

    # create a salt value
    chars = []
    for i in range(8):
        chars.append(random.choice(alphanum))
    salt = "".join(chars)
    pwd += salt
    hashed_pwd = hashlib.sha256(pwd.encode()).hexdigest()
    response = table.put_item(
        Item={
            'username': username,
            'hashed_pwd': hashed_pwd,
            'salt': salt
        }
    )
    # add to the session
    session['authenticated'] = True
    session['username'] = username

    return render_template("register_success.html", title="Flim - Successfully Registered", username=username)


@webapp.route('/login_submit', methods=['POST'])
def login_submit():
    """
    
    :return: 
    """
    username = request.form.get('username', '')
    pwd = request.form.get('password', '')
    # connect to database
    table = dynamodb.Table('users')
    # check if the account exists
    response = table.query(
        KeyConditionExpression=Key('username').eq(username)
    )
    error = False
    error_msg = ""
    if response['Count'] == 0:
        error = True
        error_msg = "Error: Username doesn't exist!"
    if error:
        return render_template("main.html",title="Flim", login_block="yes", login_error_msg=error_msg)

    # if exists, is password correct?
    salt = response['Items'][0]['salt']
    hashed_pwd = response['Items'][0]['hashed_pwd']
    pwd += salt
    if hashed_pwd == hashlib.sha256(pwd.encode()).hexdigest():
        # login successfully
        # add to the session
        session['authenticated'] = True
        session['username'] = username
        return redirect(url_for('home_page', username=username))
    else:
        error = True
        error_msg = "Error: Wrong password or username! Please try again!"
    if error:
        return render_template("main.html", title="Flim", login_block="yes", login_error_msg=error_msg)


@webapp.route('/logout', methods=['GET'])
def logout():
    """
    Log out from the current account
    :return: welcome page
    """
    session.clear()
    return redirect(url_for('main'))

