from flask import Blueprint, current_app
import requests
import datetime
import re
import humanize
import json


class JenkinsClient():

    def __init__(self, app=None):
        self.jenkins_host = app.config.get('JENKINSURL')
        self.headers = {'content-type': 'application/json'}
        blueprint = Blueprint("jenkins_client", __name__)
        app.register_blueprint(blueprint)

    def get_buildtime(self, service):
        url = '%s/job/%s-prod/api/json?tree=builds[*]' % \
              (self.jenkins_host, service)
        #current_app.logger.debug("JenkinsTime url: %s" % url)
        results = requests.get(url)
        times = results.json()['builds']
        jenkinstimes = [
            {
                "duration": time['duration'],
                "display": time['fullDisplayName'],
            } for time in times
            ]

        for jenkinstime in jenkinstimes:
            if jenkinstime['duration'] > 0:
                jenkinstime['duration'] = str(datetime.timedelta(milliseconds=jenkinstime['duration']))[:-7]

        #current_app.logger.debug("JenkinsTime3333 url: %s" % jenkinstime['duration'])

        return jenkinstimes

    def get_latestbuild(self, service):
        url = '%s/job/%s-prod/lastBuild/api/json' % \
              (self.jenkins_host, service)
        current_app.logger.debug("JenkinsBuild url: %s" % url)
        results = requests.get(url)
        builds = results.json()['result']


        current_app.logger.debug("JenkinsBuild67674 url: %s" % builds)

        return builds

    def get_latestversion(self, service):
        url = '%s/job/%s-prod/lastBuild/api/json' % \
              (self.jenkins_host, service)
        current_app.logger.debug("JenkinsBuild url: %s" % url)
        results = requests.get(url)
        version = results.json()['displayName']

        current_app.logger.debug("JenkinsBuild67674 url: %s" % version)

        return version

    #def get_jenkinsgitsource(self, service):
        #url = '%s/job/%s-prod/lastBuild/api/json?pretty=true&tree=actions[remoteUrls[*]]' % \
              #(self.jenkins_host, service)
        #current_app.logger.debug("JenkinsBuild url: %s" % url)
        #results = requests.get(url, headers=self.headers)
        #current_app.logger.debug("JenkinsBuild67645454574 url: %s" % results)
        #jgitsource = results.json()['actions']
        #current_app.logger.debug("JenkinsBuild655555555 url: %s" % jsource)
        #jgitsource = (", ".join(jsource))
        #jgitsource = jstring.replace('git', 'http', 1)
        #current_app.logger.debug("JenkinsBuild655555555 url: %s" % jgitsource)


        #current_app.logger.debug("JenkinsBuild67645454574 url: %s" % jgitsource['giturl'])

        #return jgitsource