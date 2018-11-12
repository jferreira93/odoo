# -*- coding: utf-8 -*-

from odoo import models, api
import odoo.addons.crm.models.crm_lead as crm_models_crm_lead

import logging

_logger = logging.getLogger(__name__)

class request_module(crm_models_crm_lead.Lead):
    @api.multi
    def action_set_won(self):
        """ Won semantic: probability = 100 (active untouched) """
        logging.warning("Mark as won! new %s", self)
        for lead in self:
            stage_id = lead._stage_find(domain=[('probability', '=', 100.0), ('on_change', '=', True)])
            lead.write({'stage_id': stage_id.id, 'probability': 100})

        return True
