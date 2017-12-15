from flask import render_template, request, session, redirect, url_for
from app import webapp
import boto3
from boto3.dynamodb.conditions import Key, Attr

@webapp.route('/tests', methods=['GET'])
def tests_module():
    return


