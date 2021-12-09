from odoo import api, fields, models
from datetime import datetime

class CashBankingConfirm(models.TransientModel):
    _name = "cash_managment.cash_banking_confirm"
    _description = "Confirm"
    _rec_name = 'state'

    
    state = fields.Selection([('New', 'New'),('reject_one','Rejected'),('reject_two','Rejected'),('approved','Approved'),('initiated','Initiated'),('confirm', 'Confirmed'),('expired_branch','Expired'),('expired_hod','Expired')],default="initiated", string="Status")
    from_manager_comment = fields.Text(string="Comment")
    from_manager_date =  fields.Datetime(string='Date', default=lambda self: fields.datetime.now())
   
    
    @api.multi
    def cash_confirm_cash_banking(self):
        self.write({'state': 'approved'})
        cash = self.env['cash_managment.cash_branch_bank_request'].browse(self._context.get('active_ids'))
        for req in cash:
            req.state = self.state
            req.to_manager_comment = self.from_manager_comment
            req.to_manager_date = self.from_manager_date

            template_id = self.env.ref('cash_managment.email_template_branch_bank_request_supervise').id
            template =  self.env['mail.template'].browse(template_id)
            template.send_mail(req.id,force_send=True)
         
