from odoo import models, fields

class MobileServiceLine(models.Model):
    _name = 'mobile.service.line'
    _description = 'Service Line Item'

    service_id = fields.Many2one('mobile.service', string="Service Request")
    category = fields.Char(string="Category")
    description = fields.Text(string="Description")