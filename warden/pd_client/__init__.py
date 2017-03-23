from flask import Blueprint, current_app
import requests
from datetime import datetime, timedelta
import json
import subprocess
import re

STATUSES = 'acknowledged'

class PagerdutyClient():

    def __init__(self, app=None):
        self.pd_host = app.config.get('PDURL')
        self.pd_token = app.config.get('PDTOKEN')
        self.headers  = {'Content-type': 'application/json'}
        blueprint = Blueprint("pd_client", __name__)
        app.register_blueprint(blueprint)

    def get_triggered(self):
        url = '%s/incidents' % \
        (self.pd_host)
        self.api_version = '2'
        self.auth = {'Accept': 'application/vnd.pagerduty+json;version=' + self.api_version,
                     'Authorization': 'Token token=' + self.pd_token, 'Content-type': 'application/json'}
        current_app.logger.debug("PD url: %s" % url)
        payload = {
            'statuses': STATUSES,
        }

        results = requests.get(url, headers=self.auth, params=json.dumps(payload))
        incidents = results.json()['incidents']
        triggered = [
            {
                'incident_id': incident['id'],
                'service_name': incident['service']['summary'],
                'status': incident['status'],
                #'totals': incident['total']
            } for incident in incidents
            ]
        current_app.logger.debug("PD request: %s" % triggered)
        return triggered

    def get_count(self):
        reqstrig = subprocess.Popen([
            "curl", "-sSfL", "-H", "Accept: application/vnd.pagerduty+json;version=2", "-H", "Content-type: application/json",
            "-H", "Authorization: Token token=BuLKbiqpzB4xqw4v35hn", "-X", "GET", "-G", "https://api.pagerduty.com/incidents/count?statuses%5B%5D=triggered"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        curlstdouttrig, curlstderrtrig = reqstrig.communicate()
        optrig = str(curlstdouttrig)
        therealtrig = re.findall("\d", optrig)[0]
        trigint = int(therealtrig)

        reqsack = subprocess.Popen([
            "curl", "-sSfL", "-H", "Accept: application/vnd.pagerduty+json;version=2", "-H",
            "Content-type: application/json",
            "-H", "Authorization: Token token=BuLKbiqpzB4xqw4v35hn", "-X", "GET", "-G",
            "https://api.pagerduty.com/incidents/count?statuses%5B%5D=acknowledged"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        curlstdoutack, curlstderrack = reqsack.communicate()
        opack = str(curlstdoutack)
        therealack = re.findall("\d", opack)[0]
        ackint = int(therealack)

        problemset = [trigint, ackint]
        problemsum = sum(list(problemset))

        return problemsum

    def get_statusbyservice(self):
        url = '%s/incidents' % \
              (self.pd_host)
        self.api_version = '2'
        self.auth = {'Accept': 'application/vnd.pagerduty+json;version=' + self.api_version, 'Authorization': 'Token token={0}'.format(self.pd_token), 'Content-type': 'application/json'}
        current_app.logger.debug("PD_Service url: %s" % url)
        payload = {
            'statuses': STATUSES,
            'since': (datetime.now() + timedelta(6*365/12)).strftime('%Y-%m-%d'),
            'until': datetime.now().strftime('%Y-%m-%d')
        }

        results = requests.get(url, headers=self.auth, params=json.dumps(payload))
        incidents = results.json()['incidents']
        statusbyservice = [
            {
                'incident_id': incident['id'],
                'service_name': incident['service']['summary'],
                'status': incident['status'],
                'escalation_policy': incident['escalation_policy']['summary'],
            } for incident in incidents
            ]
        current_app.logger.debug("PD_by_service: %s" % statusbyservice)
        return statusbyservice

    def get_servicestats(self, service):
        url = '%s/incidents' % \
              (self.pd_host)
        self.api_version = '2'
        self.auth = {'Accept': 'application/vnd.pagerduty+json;version=' + self.api_version,
                     'Authorization': 'Token token={0}'.format(self.pd_token), 'Content-type': 'application/json'}
        #current_app.logger.debug("PD_Service url: %s" % url)
        payload = {
            'statuses': STATUSES,
            'since': (datetime.now() + timedelta(6 * 365 / 12)).strftime('%Y-%m-%d'),
            'until': datetime.now().strftime('%Y-%m-%d')
        }

        results = requests.get(url, headers=self.auth, params=json.dumps(payload))
        incidents = results.json()['incidents']
        servicestats = [
            {
                'incident_id': incident['id'],
                'service_name': incident['service']['summary'],
                'status': incident['status'],
                'escalation_name': incident['escalation_policy']['summary'],
            } for incident in incidents
            ]
        for servicestat in servicestats:
          escname = servicestat['escalation_name']
          regex = re.compile('%s' % escname, re.I)
          match = re.match(regex, str(service))
          if match is not None:
            servicestat['escalation_name'] = "Sammy"

        #current_app.logger.debug("PD_by_service11111444444: %s" % servicestat['escalation_name'])
        return servicestats