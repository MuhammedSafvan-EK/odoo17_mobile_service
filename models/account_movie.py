from odoo import models, fields, api
import qrcode
import base64
from io import BytesIO

class AccountMove(models.Model):
    _inherit = 'account.move'

    mobile_service_id = fields.Many2one('mobile.service', string="Service Reference")
    qr_code = fields.Binary("QR Code", compute="_generate_qr_code", store=True)

    @api.depends('name', 'amount_total', 'invoice_date')
    def _generate_qr_code(self):
        for record in self:
            if record.name and record.amount_total:
                qr = qrcode.QRCode(box_size=10, border=4)
                qr.add_data(f"Invoice: {record.name}\nAmount: {record.amount_total}\nDate: {record.invoice_date}")
                qr.make(fit=True)
                img = qr.make_image(fill_color="black", back_color="white")
                buffer = BytesIO()
                img.save(buffer, format="PNG")
                qr_code_b64 = base64.b64encode(buffer.getvalue())
                record.qr_code = qr_code_b64
            else:
                record.qr_code = False
