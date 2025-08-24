from odoo import models, fields,api

class MobilePartsLine(models.Model):
    _name = 'mobile.parts.line'
    _description = 'Parts Used Line'

    service_id = fields.Many2one('mobile.service', string="Service")
    product_id = fields.Many2one('product.template', string="Product",required=1)
    qty = fields.Float(string="Qty",default=1.0)
    unit_price = fields.Float(string='Unit Price',related='product_id.list_price',readonly=1)
    on_hand_qty=fields.Float(string='On Hand',related='product_id.qty_available',readonly=1)
    subtotal = fields.Float(string='Price',compute="_compute_subtotal", store=True)

    @api.depends('qty', 'unit_price')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.qty * line.unit_price

