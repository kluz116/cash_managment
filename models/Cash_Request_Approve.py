from odoo import models, fields, api
 
class CashRequestApprove(models.Model):
    _inherit = 'cash_managment.request_confirmation'

    @api.model
    def create(self, values):
        res = super(CashRequestApprove, self).create(values)
        
        cash = self.env['cash_managment.requestapproved'].browse(self._context.get('active_ids'))
        for req in res:
            req.initiated_request_id.state = 'closed'
        #template_id = self.env.ref('cash_managment.email_template_create_request').id
        #template =  self.env['mail.template'].browse(template_id)
        #template.send_mail(res.id,force_send=True)
        return res
