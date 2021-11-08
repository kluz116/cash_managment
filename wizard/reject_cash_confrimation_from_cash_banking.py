from odoo import api, fields, models
from datetime import datetime

class CashRejectBanking(models.TransientModel):
    _name = "cash_managment.reject_cash_confirmation_banking"
    _description = "Reject Cash Request"
    _rec_name = 'state'

    
    state = fields.Selection([('pending', 'Pending'),('reject', 'Reject'),('closed', 'Closed')],default="pending", string="Status")
    reject_comment_one= fields.Text(string="Reject Comment")
    reject_date_one =  fields.Datetime(string='Reject Date', default=datetime.today())
    rejected_by_one = fields.Many2one('res.users','Canceled By')
    
    @api.multi
    def reject_cash_confirmation_bankingx(self):
        self.write({'state': 'reject'})
        cash = self.env['cash_managment.cash_bank_request_confirmation'].browse(self._context.get('active_ids'))
        for req in cash:
            req.state = self.state
       
   
