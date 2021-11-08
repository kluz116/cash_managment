from odoo import api, fields, models
from datetime import datetime

class CashRejectBranchBank(models.TransientModel):
    _name = "cash_managment.reject_cash_confirmation_branch_bank"
    _description = "Reject Cash Request"
    _rec_name = 'reject_comment_one'

    state = fields.Selection([('New', 'New'),('reject_one','Reject'),('ongoing','Ongoing'),('closed', 'Closed'),('expired_branch','Expired'),('expired_hod','Expired')],default="reject_one", string="Status")
    #state = fields.Selection([('ongoing', 'Pending Manager Approval'),('reject_one','Rejected'),('confirmed_one', 'Pending Accountant Approval'),('confirmed_two', 'Pending Manager Approval'),('confirmed_three', 'Confirmed')],default="reject_one", string="Status")
    reject_comment_one= fields.Text(string="Reject Comment")
    reject_date_one =  fields.Datetime(string='Reject Date', default=datetime.today())
    rejected_by_one = fields.Many2one('res.users','Canceled By',default=lambda self: self.env.user)
    

    @api.multi
    def reject_cash_confirmation_branch_bank_(self):
        self.write({'state': 'reject_one'})
        cash = self.env['cash_managment.cash_branch_bank_request'].browse(self._context.get('active_ids'))
        for req in cash:
            req.state = self.state
            req.reject_comment_one = self.reject_comment_one
            req.reject_date_one = self.reject_date_one
            req.rejected_by_one = self.rejected_by_one
              
        
