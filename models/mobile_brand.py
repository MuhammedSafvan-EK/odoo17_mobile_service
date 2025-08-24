from odoo import models,fields

class MobileBrand(models.Model):
    _inherit = "product.template"

    in_warranty=fields.Boolean(string='In_warranty')