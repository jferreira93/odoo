# -*- coding: utf-8 -*-

from odoo import api, models
import logging
import requests
import json

_logger = logging.getLogger(__name__)

class Lead(models.Model):
    _inherit = "crm.lead"

    @api.multi
    def action_set_won(self):
        """ Won semantic: probability = 100 (active untouched) """

        for lead in self:
            r = self.prepare_new_project_request(lead)
            r.json()
            stage_id = lead._stage_find(domain=[('probability', '=', 100.0), ('on_change', '=', True)])
            lead.write({'stage_id': stage_id.id, 'probability': 100})

        return True

    def create_identifier(self, lead_name):
        identifier = lead_name.replace(" ", "_").lower()
        identifier += '_a1'

        return identifier

    def prepare_new_project_request(self, lead):
        identifier = self.create_identifier(lead.name)
        url = "http://localhost:3000/projects.json"
        data = { "project": { "name": lead.name, "identifier": identifier } }
        headers = {"Content-type": "application/json", "X-Redmine-API-Key": "ce60ab267dc411a725b0f36a77fe4097dc118542"}
        r = requests.post(url, data=json.dumps(data), headers=headers)

        return r
