# -*- coding: utf-8 -*- 
if 0:
    from gluon.globals import *
    from gluon.html import *
    from gluon.http import *
    from gluon.sqlhtml import SQLFORM, SQLTABLE, form_factory
    session = Session()
    request = Request()
    response = Response()
#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################  

@auth.requires_login()
def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html
    """
    form = SQLFORM(db.notes, fields=['content'], _name='myform', showid=True,
                   labels = {'content': 'Your notes'}, hidden=dict(lat="", lng=""))
    if form.accepts(request.vars, session):
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'
    response.flash = T('Welcome to web2py')
    return dict(form=form, message=T('Hello World'))


def user():
    """
    exposes:
    http://..../[app]/default/user/login 
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request,db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    session.forget()
    return service()

@auth.requires_login()
def post():
    print(request.vars)
    return TR(TD(request.vars.lat), TD("_"), TD(request.vars.lng), TD("_"), TD(request.vars.content))
    
@service.json
def getNotes(lat, lng):
    """
    Get notes based on geolocation
    """
    result = {'notes':[{'title':'test1',
                        'description':'test1',
                        'lat': (float(lat) - 0.001),
                        'lng': (float(lng) - 0.001)},
                        {'title':'test2',
                        'description':'test2',
                        'lat': (float(lat) + 0.001),
                        'lng': (float(lng) + 0.001)}]}
    print('%s : %s' % (lat, lng))
    return result