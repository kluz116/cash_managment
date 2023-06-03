from odoo import api, fields, models
from datetime import datetime

class CashBankingConfirmManagerFinal(models.TransientModel):
    _name = "cash_managment.cash_banking_manager_confirm_final"
    _description = "Confirm"
    _rec_name = 'state'

    
    state = fields.Selection([('New', 'New'),('reject_one','Rejected'),('reject_two','Rejected'),('approved','Approved'),('initiated','Initiated'),('confirm', 'Confirmed'),('confirm_final', 'Confirmed'),('expired_branch','Expired'),('expired_hod','Expired')],default="confirm", string="Status")
    from_comment_manager = fields.Text(string="Comment")
    from_date_manager =  fields.Datetime(string='Date', default=lambda self: fields.datetime.now())

    @api.multi
    def cash_confirm_cash_banking_final_manager(self):
        self.write({'state': 'confirm_final'})
        cash = self.env['cash_managment.cash_branch_bank_request'].browse(self._context.get('active_ids'))
        for req in cash:
            req.state = self.state
            req.from_comment_manager = self.from_comment_manager
            req.from_date_manager = self.from_date_manager

            template_id = self.env.ref('cash_managment.email_template_pending_confirmation_banking_accountant_confirmed').id
            template =  self.env['mail.template'].browse(template_id)
            template.send_mail(req.id,force_send=True)
         
