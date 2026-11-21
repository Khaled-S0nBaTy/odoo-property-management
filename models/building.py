from odoo import models, fields


class Building(models.Model):
    _name = "building"
    _description = "Building"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    no = fields.Char()
    code = fields.Text()
    description = fields.Char()
    active = fields.Boolean(default=True)
