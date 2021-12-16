from odoo import api, fields, models
from datetime import datetime

class CashBankingConfirmFinal(models.TransientModel):
    _name = "cash_managment.cash_banking_confirm_final"
    _description = "Confirm"
    _rec_name = 'state'

    
    state = fields.Selection([('New', 'New'),('reject_one','Rejected'),('reject_two','Rejected'),('approved','Approved'),('initiated','Initiated'),('confirm', 'Confirmed'),('expired_branch','Expired'),('expired_hod','Expired')],default="confirm", string="Status")
    from_comment = fields.Text(string="Comment")
    from_date =  fields.Datetime(string='Date', default=lambda self: fields.datetime.now())
    trx_proof = fields.Binary(string='Upload file', attachment=True)
   
    
    @api.multi
    def cash_confirm_cash_banking_final(self):
        self.write({'state': 'confirm'})
        cash = self.env['cash_managment.cash_branch_bank_request'].browse(self._context.get('active_ids'))
        for req in cash:
            req.state = self.state
            req.from_comment = self.from_comment
            req.from_date = self.from_date
            req.trx_proof = self.trx_proof

            template_id = self.env.ref('cash_managment.email_template_branch_bank_request_confirm').id
            template =  self.env['mail.template'].browse(template_id)
            template.send_mail(req.id,force_send=True)
         
