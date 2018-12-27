# -*- coding: utf-8 -*-

from odoo import api, models, http, _
import logging
import requests
import json
from odoo.http import request

_logger = logging.getLogger(__name__)

class Lead(models.Model):
    _inherit = "crm.lead"

    @api.multi
    def action_set_won(self):
        """ Won semantic: probability = 100 (active untouched) """
        session_id = self.get_session_id()
        for lead in self:
            attachments = self.get_lead_attachments(lead.id)
            for attachment in attachments:
                file_url = self.create_file_url(attachment.id, attachment.name)
                self.download_attachment(file_url, attachment.name, session_id)
            r = self.prepare_new_project_request(lead.name)
            r.json()
            # upload all attachments to project in Redmine
            stage_id = lead._stage_find(domain=[('probability', '=', 100.0), ('on_change', '=', True)])
            lead.write({'stage_id': stage_id.id, 'probability': 100})
        return True

    def get_session_id(self):
        return request.session.sid

    def get_lead_attachments(self, lead_id):
        attachments = self.env['ir.attachment'].search([('res_model', '=', self._name), ('res_id', '=', lead_id)])
        return attachments

    def create_file_url(self, att_id, att_name):
        file_url = "http://localhost:8069/web/content/{0}/{1}".format(att_id, att_name)
        return file_url

    def download_attachment(self, url, att_name, session_id):
        cookies = {'session_id': session_id}
        r = requests.get(url, cookies=cookies)
        download_path = "/Users/juan/temp_odoo/{0}".format(att_name)
        with open(download_path, 'wb') as f:
            f.write(r.content)

    def prepare_new_project_request(self, lead_name):
        identifier = self.create_identifier(lead_name)
        url = "http://localhost:3000/projects.json"
        data = { "project": { "name": lead_name, "identifier": identifier } }
        headers = { "Content-type": "application/json", "X-Redmine-API-Key": "1b36cd093120c762c4b8e049dd065e8f6a3d69d5" }
        r = requests.post(url, data=json.dumps(data), headers=headers)
        return r

    def create_identifier(self, lead_name):
        identifier = lead_name.replace(" ", "_").lower()
        identifier += '_a1'
        return identifier
