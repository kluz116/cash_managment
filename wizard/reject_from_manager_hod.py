from odoo import api, fields, models
from datetime import datetime

class CashRejectHod(models.TransientModel):
    _name = "cash_managment.reject_cash_confirmation_hod"
    _description = "Reject Cash Request"
    _rec_name = 'reject_comment_one'

    
    state = fields.Selection([('ongoing', 'Pending Manager Confirmation From'),('reject_one','Rejected'),('confirmed_three', 'Confirmed')],default="ongoing", string="Status")
    reject_comment_one= fields.Text(string="Reject Comment")
    reject_date_one =  fields.Datetime(string='Reject Date', default=datetime.today())
    rejected_by_one = fields.Many2one('res.users','Canceled By',default=lambda self: self.env.user)
    

    @api.multi
    def reject_cash_confirmation_hod(self):
        self.write({'state': 'reject_one'})
        cash = self.env['cash_managment.request_confirmation_bank_hod'].browse(self._context.get('active_ids'))
        for req in cash:
            req.state = self.state
            req.reject_comment_one = self.reject_comment_one
            req.reject_date_one = self.reject_date_one
            req.rejected_by_one = self.rejected_by_one
            req.initiated_request_id.state = 'rejected'
            
              

        
