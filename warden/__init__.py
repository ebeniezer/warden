from flask import Flask, render_template, request, session, g
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.exc import DBAPIError
from flask_bootstrap import Bootstrap
import logging
from logging.handlers import RotatingFileHandler
import requests

app = Flask(__name__)
app.config.from_object('warden.local_settings')

handler = RotatingFileHandler(app.config['LOGGING_LOCATION'], maxBytes=100000000, backupCount=3)
handler.setLevel(app.config['LOGGING_LEVEL'])
formatter = logging.Formatter(app.config['LOGGING_FORMAT'])
handler.setFormatter(formatter)
app.logger.addHandler(handler)

db = SQLAlchemy(app)

# Bootstrap
Bootstrap(app)

#DB
app.db = db

import cortex_client
c_client = cortex_client.CortexClient(app)

import ntf_client
ntf_client = ntf_client.NtfClient(app)

import pd_client
pd_client = pd_client.PagerdutyClient(app)

import pingdom_client
pingdom_client = pingdom_client.PingdomClient(app)

import jira_client
jira_client = jira_client.JiraClient(app)

import graphite_client
graphite_client = graphite_client.GraphiteClient(app)

import jenkins_client
jenkins_client = jenkins_client.JenkinsClient(app)

from .application import application_blueprint
app.register_blueprint(application_blueprint)

#import warden.json_logger as json_logger
#json_logger.JsonLogger(app)

from warden.models import *
from warden.forms import *

db.create_all()
db.session.commit()

@app.before_request
def before_request():
    """ Test the db connection before we do anything else """
    try:
        db.engine.execute("SELECT 1")
    except DBAPIError, e:
        app.logger.warn(e)
        app.logger.warn("Reconnecting")
        db.session.connection = db.engine.connect()


@app.route('/')
def index():
    return application.views.dashboard()
