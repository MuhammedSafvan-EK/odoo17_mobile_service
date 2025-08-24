from datetime import date
from odoo import models, fields, api
from odoo.exceptions import UserError


class MobileService(models.Model):
    _name = "mobile.service"  # must match in xml file <field name="model">--must match-</field>
    _inherit = ['mail.thread', 'mail.activity.mixin']  # Enable chatter and activities
    _description = "mobile service details"

    # Company details
    company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.company, readonly=1)
    company_logo = fields.Binary(string='Company Logo', readonly=1, related='company_id.logo')
    contact_number = fields.Char(string='Contact Number', readonly=1, related='company_id.phone')
    email = fields.Char(string='Email', readonly=1, related='company_id.email')
    location = fields.Char(string='Location', readonly=1, related='company_id.street')
    service_type = fields.Selection([
        ('repair', 'Repair'),
        ('in warranty', 'In Warranty'),
    ], string='Service Type', default='repair', required=1)
    status_bar = fields.Selection([
        ('draft', 'DRAFT'),
        ('assigned', 'ASSIGNED'),
        ('in_progress', 'IN PROGRESS'),
        ('returned', 'RETURNED'),
        ('completed', 'COMPLETED'),
    ], default='draft', string="Status", tracking=1)
    # Auto-generated sequence number for each service record
    sequence_num = fields.Char(string='Service ID', required=1, readonly=1, copy=0, default=lambda self: 'New')
    # Customer information
    customer_name = fields.Many2one('res.partner', string='Customer Name', required=1, tracking=True)
    number = fields.Char(string='Customer Number', related='customer_name.phone', required=1)
    customer_email = fields.Char(string='Email', related='customer_name.email')
    customer_address = fields.Char(string='City', related='customer_name.street')
    req_date = fields.Date(string='Requested Date', default=date.today(), required=1)
    return_date = fields.Date(string='Return Date',required=1)
    is_technician = fields.Many2one('res.users', string='Technician', required=1, domain="[('technician','=',True)]")
    # This filters the dropdown list to show only users who have the technician field set to True.
    in_warranty = fields.Many2one('product.template', string='Mobile Brand', required=1,
                                  domain="[('in_warranty','=',True)]")
    # Notebook session
    # page1
    imei_number = fields.Char(string='IMEI Number')
    internal_note = fields.Text(string='Internal Notes')
    # page2
    service_line_ids = fields.One2many('mobile.service.line', 'service_id', string="Service Lines")
    # page3
    parts_used_ids = fields.One2many('mobile.parts.line', 'service_id', string="Parts Used")
    total_amount = fields.Float(string="Grand Total", compute="_compute_total_amount", store=True)
    # page4(media or doc)
    media_document = fields.Many2many(
        'ir.attachment',
        'mobile_service_attachment_rel',
        'service_id',
        'attachment_id',
        string="Document")
    # invoice payment status
    invoice_id = fields.Many2one('account.move', string='Invoice')
    invoice_payment_status = fields.Selection([
        ('paid', 'Paid'),
        ('not_paid', 'Not Paid')],
        string='Payment Status', compute='_compute_invoice_payment_status', store=True)

    # invoice payment status
    @api.depends('invoice_id.payment_state')
    def _compute_invoice_payment_status(self):
        for record in self:
            if record.invoice_id and record.invoice_id.payment_state == 'paid':
                record.invoice_payment_status = 'paid'
            else:
                record.invoice_payment_status = 'not_paid'

    # page3: grand total session
    @api.depends('parts_used_ids.subtotal')
    def _compute_total_amount(self):
        for rec in self:
            rec.total_amount = sum(line.subtotal for line in rec.parts_used_ids)

    # sequence num
    @api.model
    def create(self, vals):
        if vals.get('sequence_num', 'New') == 'New':
            vals['sequence_num'] = self.env['ir.sequence'].next_by_code('mobile.service') or 'New'
        return super(MobileService, self).create(vals)

    # buttons functions and status bar action
    def action_assign_technician(self):
        self.status_bar = 'assigned'

    def action_print_ticket(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'What do you want to do?',
            'view_mode': 'form',
            'res_model': 'service.print.wizard',
            'target': 'new',
            'context': {
                'default_service_id': self.id,
            },
        }

    def action_in_progress(self):
        self.status_bar = 'in_progress'

    def action_completed(self):
        self.status_bar = 'completed'

    def action_returned(self):
        self.status_bar = 'returned'

    # integrate invoice with invoicing module
    def action_generate_invoice(self):
        self.ensure_one()

        invoice_lines = []
        for part in self.parts_used_ids:
            invoice_lines.append((0, 0, {
                'product_id': part.product_id.id,
                'quantity': part.qty,
                'price_unit': part.unit_price,
            }))

        invoice = self.env['account.move'].create({
            'move_type': 'out_invoice',  # Customer invoice
            'partner_id': self.customer_name.id,
            'invoice_date': fields.Date.context_today(self),
            'invoice_line_ids': invoice_lines,
        })
        # Link the invoice to this service
        self.invoice_id = invoice.id
        return {
            'type': 'ir.actions.act_window',
            'name': 'Customer Invoice',
            'res_model': 'account.move',
            'view_mode': 'form',
            'res_id': invoice.id,
            'target': 'current',
        }

    #user error
    @api.constrains('return_date', 'req_date')
    def _check_return_date(self):
        for rec in self:
            if rec.return_date and rec.return_date < rec.req_date:
                raise UserError("Return Date cannot be earlier than Request Date.")