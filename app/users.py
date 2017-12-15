from flask import render_template, request, session, redirect, url_for
from app import webapp
import boto3
from boto3.dynamodb.conditions import Key, Attr


@webapp.route('/home/<username>', methods=['GET'])
def home_page(username):
    """
    
    :param username: 
    :return: 
    """
    # check if the current user logged in
    if 'authenticated' not in session:
        # tourist
        return redirect(url_for('others_home', username=username, user_self=None))
    if session['username'] != username:
        # visit other's home
        return redirect(url_for('others_home', username=username, user_self=session['username']))

    # your stuff


def others_home(username,user_self):
    """
    
    :param username: 
    :param self: 
    :return: 
    """

    # other's stuff