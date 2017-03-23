# This client was used to test providing graphical views of systems level activities
# Praxis is the name of a VM

from flask import Blueprint, current_app
import requests
import time

class GraphiteClient():
    def __init__(self, app=None):
        self.graphite_host = app.config.get('GRAPHITEURL')
        self.graphite_from = app.config.get('GRAPHITEFROM')
        self.graphite_until = app.config.get('GRAPHITEUNTIL')
        self.graphite_height = app.config.get('GRAPHITEHEIGHT')
        self.graphite_width = app.config.get('GRAPHITEWIDTH')
        self.headers  = {'Content-type': 'application/json'}
        blueprint = Blueprint("graphite_client", __name__)
        app.register_blueprint(blueprint)

    def get_cpuload(self):
        url = '%s/render/?width=%s&height=%s&from=%s&until=%s&target=systems.prod-praxis*.load.load.midterm&format=png' % \
        (self.graphite_host, self.graphite_width, self.graphite_height, self.graphite_from, self.graphite_until)

        #current_app.logger.debug("GRAPHITE url: %s" % url)

        results = requests.get(url)

        current_app.logger.debug("GRAPHITE: %s" % results)
        return results
