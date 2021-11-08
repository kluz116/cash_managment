from odoo import api, fields, models
from datetime import datetime

class CashRejectBranchBankTwo(models.TransientModel):
    _name = "cash_managment.reject_cash_confirmation_branch_bank_two"
    _description = "Reject Cash Request"
    _rec_name = 'reject_comment_two'

    state = fields.Selection([('New', 'New'),('reject_one','Reject'),('reject_two','Reject'),('ongoing','Ongoing'),('closed', 'Closed'),('expired_branch','Expired'),('expired_hod','Expired')],default="reject_two", string="Status")
    #state = fields.Selection([('ongoing', 'Pending Manager Approval'),('reject_one','Rejected'),('confirmed_one', 'Pending Accountant Approval'),('confirmed_two', 'Pending Manager Approval'),('confirmed_three', 'Confirmed')],default="reject_one", string="Status")
    reject_comment_two= fields.Text(string="Reject Comment")
    reject_date_two =  fields.Datetime(string='Reject Date', default=datetime.today())
    rejected_by_two = fields.Many2one('res.users','Canceled By',default=lambda self: self.env.user)
    

    @api.multi
    def reject_cash_confirmation_branch_bank_two_(self):
        self.write({'state': 'reject_two'})
        cash = self.env['cash_managment.cash_branch_bank_request'].browse(self._context.get('active_ids'))
        for req in cash:
            req.state = self.state
            req.reject_comment_two = self.reject_comment_two
            req.reject_date_two = self.reject_date_two
            req.rejected_by_two = self.rejected_by_two
              
        
