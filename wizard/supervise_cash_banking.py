from odoo import api, fields, models
from datetime import datetime

class CashBankingSupervision(models.TransientModel):
    _name = "cash_managment.supervise_cash_banking"
    _description = "Supervise Cash Request"
    _rec_name = 'state'

    
    state = fields.Selection([('New', 'New'),('ongoing','Ongoing'),('closed', 'Closed')],default="ongoing", string="Status")
    supervision_comment = fields.Text(string="Comment")
    supervision_date =  fields.Datetime(string='Cancel Date', default=datetime.today())
    supervised_by = fields.Many2one('res.users','Canceled By',default=lambda self: self.env.user)
    
    @api.multi
    def cash_banking_supervision(self):
        self.write({'state': 'closed'})
        cash = self.env['cash_managment.cash_branch_bank_request'].browse(self._context.get('active_ids'))
        for req in cash:
            req.state = self.state
            req.supervision_comment = self.supervision_comment
            req.supervision_date = self.supervision_date
            req.supervised_by = self.supervised_by
        
