from odoo import models, fields, api
 
class CashCenterNotify(models.Model):
    _inherit = 'cash_managment.cash_center_request'

    @api.model
    def create(self, values):
        res = super(CashCenterNotify, self).create(values)

        template_id = self.env.ref('cash_managment.email_template_cash_center_request').id
        template =  self.env['mail.template'].browse(template_id)
        template.send_mail(res.id,force_send=True)
        return res
