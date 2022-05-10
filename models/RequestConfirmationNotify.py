from odoo import models, fields, api
 
class CashConfirmationNotify(models.Model):
    _inherit = 'cash_managment.request_confirmation'

    @api.model
    def create(self, values):
        res = super(CashConfirmationNotify, self).create(values)

        template_id = self.env.ref('cash_managment.email_template_from_accountant_confirm_hod').id
        template =  self.env['mail.template'].browse(template_id)
        template.send_mail(res.id,force_send=True)
        return res
