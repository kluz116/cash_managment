from odoo import models, fields, api
 
class CashRequests(models.Model):
    _inherit = 'cash_managment.request'

    @api.model
    def create(self, values):
        res = super(CashRequests, self).create(values)

        template_id = self.env.ref('cash_managment.email_template_create_request').id
        template =  self.env['mail.template'].browse(template_id)
        template.send_mail(res.id,force_send=True)
        return res
