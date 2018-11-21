# -*- coding: utf-8 -*-

from odoo import api, models
import logging
import requests
import json
import requests

_logger = logging.getLogger(__name__)

class Lead(models.Model):
    _inherit = "crm.lead"

    @api.multi
    def action_set_won(self):
        """ Won semantic: probability = 100 (active untouched) """

        for lead in self:
            # get all attachments from a lead
            attachments = self.get_lead_attachments(lead.id)
            for attachment in attachments:
                logging.warning("Attachment id: %s", attachment.id)
                # generate file name
                name = attachment.name
                logging.warning("Attachment name: %s", name)
                # generate file url
                file_url = self.create_file_url(attachment)
                logging.warning("File url: %s", file_url)
                # start download file from url to /Users/juan/temp_odoo
                logging.warning("Download attachment start")
                self.download_attachment(file_url, name)

            # create a new project in Redmine
            r = self.prepare_new_project_request(lead)
            r.json()

            # upload all attachments to project in Redmine
            #  todo
            # ############################################

            # Set lead as won in Odoo
            stage_id = lead._stage_find(domain=[('probability', '=', 100.0), ('on_change', '=', True)])
            lead.write({'stage_id': stage_id.id, 'probability': 100})

        return True

    def get_lead_attachments(self, lead_id):
        attachments = self.env['ir.attachment'].search([('res_model', '=', self._name), ('res_id', '=', lead_id)])

        return attachments

    # @api.multi
    # def get_stock_file(self):
    #     return {
    #             'type' : 'ir.actions.act_url',
    #             'url': '/web/binary/download_document?model=wizard.product.stock.report&field=datas&id=%s&filename=product_stock.xls'%(self.id),
    #             'target': 'self',
    #     }

    def create_file_url(self, attachment):
        file_url = "http://localhost:8069/web/content/{0}/{1}".format(attachment.id, attachment.name)

        return file_url

    def download_attachment(self, url, name):
        r = requests.get(url)
        logging.warning("Request %s", r)
        logging.warning("Request status %s", r.status_code)

        # set download path
        download_path = "/Users/juan/temp_odoo/{0}".format(name)

        # write file in download_path
        with open(download_path, 'wb') as f:
            f.write(r.content)

    def prepare_new_project_request(self, lead):
        identifier = self.create_identifier(lead.name)
        url = "http://localhost:3000/projects.json"
        data = { "project": { "name": lead.name, "identifier": identifier } }
        headers = {"Content-type": "application/json", "X-Redmine-API-Key": "ce60ab267dc411a725b0f36a77fe4097dc118542"}
        r = requests.post(url, data=json.dumps(data), headers=headers)

        return r

    def create_identifier(self, lead_name):
        identifier = lead_name.replace(" ", "_").lower()
        identifier += '_a1'

        return identifier
