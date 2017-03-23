# NTF is our internal synthetics check tool https://github.com/shutterstock/ntf

from flask import Blueprint, current_app
import requests


class NtfClient():
    def __init__(self, app=None):
        self.ntf_host = app.config.get('NTFURL')
        self.headers  = {'content-type': 'application/json'}
        blueprint = Blueprint("ntf_client", __name__)
        app.register_blueprint(blueprint)

    def get_status(self):
        url = '%s/status' % \
        (self.ntf_host)
        current_app.logger.debug("NTF url: %s" % url)
        results = requests.get(url, headers=self.headers).json()
        stats = [
            {
                "suite": result['suite'],
                "agent": result['agent'],
                "pass":  result['pass'],
                "fail":  result['fail'],
            } for result in results
            ]
        return stats

    def get_suite(self, service):
        app_url = '%s/status' % \
        (self.ntf_host)
        current_app.logger.debug("NTF app_url: %s" % app_url)
        app_results = requests.get(app_url, headers=self.headers).json()
        app_status = [
            {
                "suite": app_result['suite'],
                "agent": app_result['agent'],
                "pass":  app_result['pass'],
                "fail":  app_result['fail'],
            } for app_result in app_results
        ]

        #for server in app_status:
            #for app in server['suite']:
                #if app.get('suite', '') == service:
                    #server['suite'] = app['suite']

        return app_status
