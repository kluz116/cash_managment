from odoo import api, fields, models
from datetime import datetime

class CashSupervision(models.TransientModel):
    _name = "cash_managment.cancel_supervision"
    _description = "Supervise Cash Request"
    _rec_name = 'state'

    
    state =  fields.Selection([('new','New'),('validate','Validated'),('cancel','Canceled'),('reject','Reject'),('approve','Approved'),('closed','Closed'),('implement','Implement')],string="Status", required=True, default="new")
    supervision_comment = fields.Text(string="Comment")
    supervision_date =  fields.Datetime(string='Cancel Date', default=lambda self: fields.datetime.now())
    supervised_by = fields.Many2one('res.users','Canceled By',default=lambda self: self.env.user)
    
    @api.multi
    def cash_supervision(self):
        self.write({'state': 'closed'})
        cash = self.env['cash_managment.request'].browse(self._context.get('active_ids'))
        for req in cash:
            req.state = self.state
            req.supervision_comment = self.supervision_comment
            req.supervision_date = self.supervision_date
            req.supervised_by = self.supervised_by
        
