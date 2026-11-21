from email.policy import default

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Property(models.Model):
    _name = "property"
    _description = "Property"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    ref = fields.Char(default="New", readonly=1)
    name = fields.Char(required=1)
    description = fields.Text(required=1, tracking=1)
    postcode = fields.Char(required=1)
    date_availability = fields.Date(tracking=1)
    expected_selling_date = fields.Date(tracking=1)
    is_late = fields.Boolean()
    expected_price = fields.Float()
    selling_price = fields.Float()
    bedrooms = fields.Integer(required=1, tracking=1)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean(tracking=1)
    garden = fields.Boolean()
    garden_area = fields.Integer()
    active = fields.Boolean(default=True)
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West'),
    ])
    owner_phone = fields.Char(related='owner_id.phone')
    owner_address = fields.Char(related='owner_id.address')

    owner_id = fields.Many2one('owner', tracking=True)
    tag_ids = fields.Many2many('tag')
    status = fields.Selection(
        [
            ("draft", "Draft"),
            ("pending", "Pending"),
            ("sold", "Sold"),
            ("closed", "Closed"),
        ],
        compute="_compute_statues",
        store=True,
        readonly=True,
    )
    bedrooms_lines_ids = fields.One2many('property.bedrooms', 'property_id')

    diff = fields.Float(compute='_compute_diff', store=True)

    _sql_constraints = [
        ('unique_name', 'unique("name")', 'This name already exists! choose another name.'),
    ]

    @api.constrains("bedrooms")
    def _check_bedrooms_not_zero(self):
        for valid_bedrooms in self:
            if valid_bedrooms.bedrooms <= 0:
                raise ValidationError(
                    "Bedrooms must be a number greater than zero."
                )

    @api.depends("owner_id")
    def _compute_statues(self):
        for property_record in self:
            if property_record.owner_id:
                property_record.status = "sold"
            else:
                property_record.status = "draft"

    @api.depends("expected_price", "selling_price")
    def _compute_diff(self):
        for rec in self:
            rec.diff = rec.expected_price - rec.selling_price

    @api.onchange("expected_price")
    def _onchange_expected_price(self):
        # for rec in self:
        return {
            'warning': {'title': 'Warning!', 'message': 'You Entered New Price !', 'type': 'notification'},
        }

    class PropertyBedrooms(models.Model):
        _name = "property.bedrooms"

        property_id = fields.Many2one('property')
        description = fields.Text(required=1)
        area = fields.Float(required=1)

    # def action_draft(self):
    #     for rec in self:
    #         rec.status = 'draft'

    def action_pending(self):
        for rec in self:
            rec.status = 'pending'

    def action_closed(self):
        for rec in self:
            rec.status = 'closed'

    def check_expected_selling_date(self):
        property_ids = self.search([])
        for rec in property_ids:
            if rec.expected_selling_date and rec.expected_selling_date < fields.Date.today():
                rec.is_late = True

    @api.model_create_multi
    def create(self, vals):
        res = super(Property, self).create(vals)
        if res.ref == 'New':
            res.ref = self.env['ir.sequence'].next_by_code('property_sequence')
        return res

    # @api.model_create_multi
    # def create(self, vals_list):
    #     rec = super().create(vals_list)
    #     if rec.ref == "New":
    #         rec.ref = self.env["ir.sequence"].next_by_code("property_sequence")
    #     return rec

    # def action_sold(self):
    #     for rec in self:
    #         rec.status = 'sold'

    # @api.model_create_multi
    # def create(self, vals_list):
    #     rec= super().create(vals_list)
    #     print("The record is created successfully !")
    #     return rec
    #
    # @api.model
    # def _search(self, domain, offset=0, limit=None, order=None , access_rights_uid=None):
    #     rec=super(Property,self). _search(domain, offset=0, limit=None, order=None, access_rights_uid=None)
    #     print("The record is searched successfully !")
    #     return rec
    #
    # @api.model
    # def write(self, vals):
    #     rec =super().write(vals)
    #     print("The record is updated successfully !")
    #     return rec
    #
    # def unlink(self):
    #     rec= super().unlink()
    #     print("The record is deleted successfully !")
    #     return rec
