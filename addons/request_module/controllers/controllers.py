# -*- coding: utf-8 -*-
from odoo import http

class RequestModule(http.Controller):
    @http.route('/request_module/request_module/', auth='public')
    def index(self, **kw):
        return "Hello, world"

    @http.route('/request_module/request_module/objects/', auth='public')
    def list(self, **kw):
        return http.request.render('request_module.listing', {
            'root': '/request_module/request_module',
            'objects': http.request.env['request_module.request_module'].search([]),
        })

    @http.route('/request_module/request_module/objects/<model("request_module.request_module"):obj>/', auth='public')
    def object(self, obj, **kw):
        return http.request.render('request_module.object', {
            'object': obj
        })
