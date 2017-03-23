from flask import Blueprint, current_app
import requests
from requests.auth import HTTPBasicAuth

class PingdomClient():
    def __init__(self, app=None):
        self.pingdom_host = app.config.get('PINGDOMURL')
        self.pingdom_token = app.config.get('PINGDOMTOKEN')
        #self.headers  = {'Content-type': 'application/json'}
        blueprint = Blueprint("pingdom_client", __name__)
        app.register_blueprint(blueprint)

    def get_checks(self):
        url = '%s/api/2.0/checks' % \
              (self.pingdom_host)
        self.header = {"App-Key" : "mz5z848bz0n2uo43hgmfbwvuek7l0pkw", "Content-type": "application/json"}
        self.user = {'dnsadmin@shutterstock.com'}
        self.psswd = {'webops'}
        current_app.logger.debug("Pingdom url: %s" % url)

        results = requests.get(url, auth=HTTPBasicAuth(self.user, self.psswd), headers=self.header)
        ping_checks = results.json()['checks']

        checks = [
            {
                'id': ping_check['id'],
                'hostname': ping_check['hostname'],
            } for ping_check in ping_checks
            ]
        current_app.logger.debug("Pingdom request: %s" % checks)
        return checks