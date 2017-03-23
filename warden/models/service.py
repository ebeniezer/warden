from warden import db
from warden.forms import ServiceEdit
from urlparse import urlparse

class Service(db.Model):
    __tablename__ = 'warden'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    in_production = db.Column(db.Boolean)
    owner = db.Column(db.String(255))
    docs = db.Column(db.Boolean)
    git_source = db.Column(db.String(255))

    def __init__(self,
                 name=name,
                 in_production=False,
                 docs=False,
                 owner=owner,
                 git_source=git_source
                 ):


      self.name = name
      self.in_production = in_production
      self.docs = docs
      self.owner = owner
      self.git_source = git_source


    def __repr__(self):
        return self.name


    def getForm(self):
        return ServiceEdit(obj=self)