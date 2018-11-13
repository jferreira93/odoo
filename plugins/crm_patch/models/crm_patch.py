# -*- coding: utf-8 -*-

from odoo import api
import logging
import odoo.addons.crm.models.crm_lead as crm_models_crm_lead

_logger = logging.getLogger(__name__)

class crm_patch(crm_models_crm_lead.Lead):

    @api.multi
    def action_set_won(self):
        """ Won semantic: probability = 100 (active untouched) """
        logging.warning("Yeeeesss! Mark as won! (plugin) %s", self)
        for lead in self:
            logging.warning("Lead name is %s", lead.name)
            logging.warning("Lead contact_name is %s", lead.contact_name)
            logging.warning("Lead description is %s", lead.description)
            logging.warning("Lead planned_revenue is %s", lead.planned_revenue)
            logging.warning("Lead create_date is %s", lead.create_date)
            logging.warning("Lead date_action_last is %s", lead.date_action_last)
            stage_id = lead._stage_find(domain=[('probability', '=', 100.0), ('on_change', '=', True)])
            lead.write({'stage_id': stage_id.id, 'probability': 100})

        return True
