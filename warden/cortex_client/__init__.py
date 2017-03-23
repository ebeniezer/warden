from flask import Blueprint, current_app
import requests
import humanize
import re
import json


class CortexClient():

    def __init__(self, app=None):
        self.cortex_host = app.config.get('CORTEX_API_HOST')
        blueprint = Blueprint("cortex_client", __name__)
        app.register_blueprint(blueprint)

    def get_servers(self, service, env_name):
        url = '%s/api/assets/find?q=shutterstock.apps.name/is:%s/environment/%s' % \
              (self.cortex_host, service, env_name)
        current_app.logger.debug("Cortex url: %s" % url)
        results = requests.get(url).json()
        servers = [
            {
                "hostname": result['name'],
                "role": result['properties']['role'],
                "status": result['status'],
                "cpu_count": result['properties']['cpu']['count'],
                "apps": result['properties']['shutterstock']['apps'],
            } for result in results
            ]

        for server in servers:
            # Make an assumption on the size based on cpu count
            # If we get the info from cortex we don't need
            # to figure out the sizes by ourselves.
            if server['cpu_count'] < 2:
                server['size'] = 'ss.small'
            elif server['cpu_count'] < 4:
                server['size'] = 'ss.medium'
            elif server['cpu_count'] >= 4:
                server['size'] = 'ss.large'
            # The data for apps is not ordered in any way
            # so only pull out the info on the app we care about
            for app in server['apps']:
                if app.get('name', '') == service:
                    server['version'] = app['version']
        return servers

    def get_serversbyservice(self, service):
        url = '%s/api/assets/find?q=shutterstock.apps.name/is:%s' % \
              (self.cortex_host, service)
        current_app.logger.debug("CortexService url: %s" % url)
        results = requests.get(url).json()
        serversbyservice = [
            {
                "hostname": result['name'],
                "role": result['properties']['role'],
                "status": result['status'],
                "cpu_count": result['properties']['cpu']['count'],
                "apps": result['properties']['shutterstock']['apps'],
                "uptime": result['properties']['uptime']
            } for result in results
            ]

        for serverbyservice in serversbyservice:
            if serverbyservice['cpu_count'] < 2:
                serverbyservice['size'] = 'ss.small'
            elif serverbyservice['cpu_count'] < 4:
                serverbyservice['size'] = 'ss.medium'
            elif serverbyservice['cpu_count'] >= 4:
                serverbyservice['size'] = 'ss.large'
            if serverbyservice['uptime'] > 0:
                serverbyservice['uptime'] = humanize.naturaltime(serverbyservice['uptime'])

        return serversbyservice

    def get_ramcount(self, service):
        url = '%s/api/assets/find?q=shutterstock.apps.name/is:%s' % \
              (self.cortex_host, service)
        current_app.logger.debug("CortexServiceRAM url: %s" % url)
        results = requests.get(url).json()

        rams = [
            {
                "total_ram": result['properties']['memory']['total']
            } for result in results
            ]
        for ram in rams:
            if ram['total_ram'] > 0:
                ram['total_ram'] = humanize.naturalsize(ram['total_ram'])

        return rams

    def app_nodecount(self):
        url = '%s/api/assets/summarize/shutterstock.apps.name' % \
              (self.cortex_host)
        current_app.logger.debug("CortexNodeCount url: %s" % url)
        numbers = requests.get(url).json()
        #numbers = json.loads(results)

        counts = [
            {
                "id": number['id'],
                "count": number['count']
            } for number in numbers
            ]

        return counts

    def get_wildcardservers(self, service):
        url = '%s/api/assets/find?q=shutterstock.apps.name/is:%s' % \
              (self.cortex_host, service)
        current_app.logger.debug("CortexShortHost url: %s" % url)
        results = requests.get(url).json()
        wildcards = [
            {
                "hostname": result['properties']['fqdn'],
                "role": result['properties']['role'],
            } for result in results
            ]

        for wildcard in wildcards:
            if wildcard['hostname'] > 0:
                wildcard['hostname'] = (re.match(r'^(\w+)-(\D+)', wildcard['hostname']).group(2) + '*')


        #current_app.logger.debug("Shortened Hostname: %s" % wildcards['hostname'])

        return wildcards
