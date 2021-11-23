from odoo import api, fields, models
from datetime import datetime

class ToMangerCashBank(models.TransientModel):
    _name = "cash_managment.to_manager_cash_bank"
    _description = "To Manager Confirm"
    _rec_name = 'state'

    
    state = fields.Selection([('pending', 'Pending'),('closed', 'Closed')],default="pending", string="Status")
    to_manager_comment = fields.Text(string="Comment")
    to_manager_date =  fields.Datetime(string='Date', default=lambda self: fields.datetime.now())
   
    
    @api.multi
    def cash_confirm_manager_cashcenter_sa(self):
        self.write({'state': 'closed'})
        cash = self.env['cash_managment.cash_bank_request_confirmation'].browse(self._context.get('active_ids'))
        for req in cash:
            req.state = self.state
            req.to_manager_comment = self.to_manager_comment
            req.to_manager_date = self.to_manager_date
         
