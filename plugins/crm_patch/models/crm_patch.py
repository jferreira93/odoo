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
            description = ['See attachments here: ']

            attachments = self.get_lead_attachments(lead.id)
            for attachment in attachments:
                logging.warning("Attachment id: %s", attachment.id)
                name = attachment.name
                logging.warning("Attachment name: %s", name)
                file_url = "http://localhost:8069/web/content/{0}/{1}".format(attachment.id, attachment.name)
                logging.warning("Description temp: %s", file_url)
                description.append(file_url)

                # self.download_attachment(attachment, file_url)



            r = self.prepare_new_project_request(lead, description)
            r.json()

            stage_id = lead._stage_find(domain=[('probability', '=', 100.0), ('on_change', '=', True)])
            lead.write({'stage_id': stage_id.id, 'probability': 100})

        return True

    def create_identifier(self, lead_name):
        identifier = lead_name.replace(" ", "_").lower()
        identifier += '_a1'

        return identifier

    def download_attachment(self, attachment, file_url):
        logging.warning("Download has to start")
        return {
            'type': 'ir.actions.act_url',
            'url': file_url,
            'target': 'new'
        }

    def prepare_new_project_request(self, lead, description):
        identifier = self.create_identifier(lead.name)
        url = "http://localhost:3000/projects.json"
        data = { "project": { "name": lead.name, "identifier": identifier, "description": description } }
        headers = {"Content-type": "application/json", "X-Redmine-API-Key": "ce60ab267dc411a725b0f36a77fe4097dc118542"}
        r = requests.post(url, data=json.dumps(data), headers=headers)

        return r

    def get_lead_attachments(self, lead_id):
        attachments = self.env['ir.attachment'].search([('res_model', '=', self._name), ('res_id', '=', lead_id)])

        return attachments

    @api.model
    def get_location(self):
        location = self.env['ir.config_parameter'].sudo().get_param('ir_attachment.location', 'file')
        logging.warning("Location: %s", location)

        return location

    @api.model
    def _full_path(self, path):
        # sanitize path
        path = re.sub('[.]', '', path)
        path = path.strip('/\\')
        return os.path.join(self._filestore(), path)

    @api.model
    def _get_path(self, bin_data, sha):
        # retro compatibility
        fname = sha[:3] + '/' + sha
        full_path = self._full_path(fname)
        if os.path.isfile(full_path):
            return fname, full_path        # keep existing path
