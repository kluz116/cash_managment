from odoo import models, fields, api
 
class CashRequestConfirmationApprove(models.Model):
    _inherit = 'cash_managment.cash_center_request_confirmation'

    @api.model
    def create(self, values):
        res = super(CashRequestConfirmationApprove, self).create(values)
        
        cash_conf_req = self.env['cash_managment.cash_center_request'].browse(self._context.get('active_ids'))
        for request in cash_conf_req:
            request.state = 'closed'

        #template_id = self.env.ref('cash_managment.email_template_create_request').id
        #template =  self.env['mail.template'].browse(template_id)
        #template.send_mail(res.id,force_send=True)
        return res
