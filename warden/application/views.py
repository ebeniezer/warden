from flask import render_template, url_for, request, redirect, current_app, flash, g, session, jsonify, json, Blueprint
from . import application_blueprint
from sqlalchemy.exc import IntegrityError
from sqlalchemy import distinct, exists, select
from warden import db, c_client, ntf_client, pd_client, pingdom_client, jenkins_client
from warden.models.service import Service
from warden.forms import ServiceEdit, ServiceNew

@application_blueprint.route('/test', methods=['GET', 'POST'])
def test_view():
  return render_template('testview.html')

@application_blueprint.route('/list', methods=['GET'])
def list():
    list = Service.query.order_by(Service.name).all()
    return render_template('list.html', list=list)

@application_blueprint.route('/new', methods=['GET', 'POST'])
def new():
    form = ServiceNew()
    if request.method == 'POST' and form.validate():
        name = form.service_name.data,
        try:
            new_service = Service(
                name=form.service_name.data,
                docs=form.docs.data,
                in_production=form.in_production.data,
                owner=form.owner.data,
                git_source=form.git_source.data,
            )
            db.session.add(new_service)
            db.session.commit()
            flash('New record added!')
            # flash("%s Added!" % new_service.name)
        except IntegrityError:
            flash("%s Was not able to be added, it apears it already exists." % name, 'danger')
        return redirect(url_for('application.service', name=name))
    else:
        return render_template('new_service.html', form=form)

@application_blueprint.route('/<name>')
def service(name):
    service = Service.query.filter(Service.name == name).first()
    docs = Service.query.filter(Service.docs).all()
    owner = Service.query.filter(Service.owner).all()
    git_source = Service.query.filter(Service.git_source).all()
    in_production = Service.query.filter(Service.in_production).all()
    servers = c_client.get_serversbyservice(name)
    rams = c_client.get_ramcount(name)
    status = ntf_client.get_suite(service)
    status = sorted(status, key=lambda app: app.get('suite'))
    wildcards = c_client.get_wildcardservers(service)
    pdservicestats = pd_client.get_servicestats(service)
    return render_template('service.html',
                           service=service,
                           docs=docs,
                           in_production=in_production,
                           owner=owner,
                           status=status,
                           servers=servers,
                           rams=rams,
                           git_source=git_source,
                           wildcards=wildcards,
                           pdservicestats=pdservicestats
                           )

@application_blueprint.route('/<name>/<env_name>/servers', methods=['GET', 'POST'])
def servers(name, env_name):
    service = Service.query.filter(Service.name == name).first()
    servers = c_client.get_servers(name, env_name)
    servers = sorted(servers, key=lambda server: server.get('hostname'))
    return render_template('appandservice.html',
                           service=service,
                           servers=servers)

@application_blueprint.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    services = Service.query.filter(Service.name).all()
    list = Service.query.order_by(Service.name).all()
    stats = ntf_client.get_status()
    pd_triggered = pd_client.get_triggered()
    pd_count = pd_client.get_count()
    pd_byservice = pd_client.get_statusbyservice()
    counts = c_client.app_nodecount()
    counts = sorted(counts, key=lambda count: count.get('id'))
    return render_template('dashboard.html',
                           services=services,
                           stats=stats,
                           pd_triggered=pd_triggered,
                           pd_count=pd_count,
                           pd_byservice=pd_byservice,
                           list=list,
                           counts=counts)
