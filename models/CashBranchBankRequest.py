from odoo import models, fields, api
 
class CashBranchBankRequest(models.Model):
    _inherit = 'cash_managment.cash_branch_bank_request'

    @api.model
    def create(self, values):
        res = super(CashBranchBankRequest, self).create(values)

        template_id = self.env.ref('cash_managment.email_template_branch_bank_request').id
        template =  self.env['mail.template'].browse(template_id)
        template.send_mail(res.id,force_send=True)
        return res
