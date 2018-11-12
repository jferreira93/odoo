# -*- coding: utf-8 -*-
from odoo import http

# class CrmPatch(http.Controller):
#     @http.route('/crm_patch/crm_patch/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/crm_patch/crm_patch/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('crm_patch.listing', {
#             'root': '/crm_patch/crm_patch',
#             'objects': http.request.env['crm_patch.crm_patch'].search([]),
#         })

#     @http.route('/crm_patch/crm_patch/objects/<model("crm_patch.crm_patch"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('crm_patch.object', {
#             'object': obj
#         })