from odoo import api, fields, models
from datetime import datetime

class CashRejectsTo(models.TransientModel):
    _name = "cash_managment.reject_cash_confirmation_to_center"
    _description = "Reject Cash Request"
    _rec_name = 'state'

    
    state = fields.Selection([('ongoing', 'Pending Manager Approval'),('reject_one','Rejected'),('confirmed_one', 'Pending Accountant Approval'),('confirmed_two', 'Pending Manager Approval'),('confirmed_three', 'Confirmed')],default="confirmed_one", string="Status")

    @api.multi
    def reject_cash_confirmation_to_cash_center(self):
        self.write({'state': 'confirmed_one'})
        cash = self.env['cash_managment.cash_center_request_confirmation'].browse(self._context.get('active_ids'))
        for req in cash:
            req.state = self.state
       
   
