from odoo import models, fields, api

class ServicePrintWizard(models.TransientModel):
    _name = 'service.print.wizard'
    _description = 'Service Print Wizard'

    service_id = fields.Many2one('mobile.service', string="Service", required=True)

    def action_print(self):
        return self.env.ref('mobile_service.action_service_report').report_action(self.service_id) #action_service_report must be similar to the service report record id

    def action_download(self):
        return self.env.ref('mobile_service.action_print_ticket').report_action(self.service_id)

    def action_open(self):
        return self.env.ref('mobile_service.action_print_ticket').report_action(self.service_id)

