from odoo import models, fields, api
 
class CashBankRequestHodNotify(models.Model):
    _inherit = 'cash_managment.cash_bank_request_hod'

    @api.model
    def create(self, values):
        res = super(CashBankRequestHodNotify, self).create(values)

        template_id = self.env.ref('cash_managment.email_template_branch_bank_request_hod').id
        template =  self.env['mail.template'].browse(template_id)
        template.send_mail(res.id,force_send=True)
        return res
