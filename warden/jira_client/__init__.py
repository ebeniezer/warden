# Incomplete

from flask import Blueprint, current_app
import requests
from requests.auth import HTTPBasicAuth

class JiraClient():
    def __init__(self, app=None):
        self.jira_host = app.config.get('JIRAURL')
        #self.headers  = {'Content-type': 'application/json'}
        blueprint = Blueprint("jira_client", __name__)
        app.register_blueprint(blueprint)
