from odoo import api, fields, models
from datetime import datetime

class CashCancel(models.TransientModel):
    _name = "cash_managment.cancel_cash"
    _description = "Reject Cash Request"
    _rec_name = 'state'

    
    state =  fields.Selection([('new','New'),('validate','Validated'),('cancel','Canceled'),('reject','Reject'),('approve','Approved'),('closed','Closed'),('implement','Implement')],string="Status", required=True, default="new")
    cancel_comment = fields.Text(string="Comment")
    cancel_date =  fields.Datetime(string='Cancel Date', default=datetime.today())
    canceled_by = fields.Many2one('res.users','Canceled By',default=lambda self: self.env.user)
    
    @api.multi
    def cash_cancel(self):
        self.write({'state': 'cancel'})
        cash = self.env['cash_managment.request'].browse(self._context.get('active_ids'))
        for req in cash:
            req.state = self.state
            req.cancel_comment = self.cancel_comment
            req.cancel_date = self.cancel_date
            req.canceled_by = self.canceled_by
        
