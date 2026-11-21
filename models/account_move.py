from odoo import models, fields


class AccountMove(models.Model):
    _inherit = 'account.move'

    property_id=fields.Many2one('property', string='Property')

    def action_post(self):
        rec = super().action_post()
        print("action done")
        return rec