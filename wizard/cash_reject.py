from odoo import api, fields, models
from datetime import datetime

class CashReject(models.TransientModel):
    _name = "cash_managment.reject_cash"
    _description = "Reject Cash Request"
    _rec_name = 'reject_comment'

    
    state =  fields.Selection([('new','New'),('validate','Validate'),('reject','Reject'),('approve','Approve'),('closed','Closed'),('implement','Implement')],string="Status", required=True, default="new")
    reject_comment = fields.Text(string="Reject Comment")
    reject_date =  fields.Datetime(string='Reject Date', default=datetime.today())
    rejected_by = fields.Many2one('res.users','Canceled By',default=lambda self: self.env.user)
    
    @api.multi
    def cash_reject(self):
        self.write({'state': 'reject'})
        cash = self.env['cash_managment.request'].browse(self._context.get('active_ids'))
        for req in cash:
            req.state = self.state
            req.reject_comment = self.reject_comment
            req.reject_date = self.reject_date
            req.rejected_by = self.rejected_by

            template_id = self.env.ref('cash_managment.email_template_reject_request').id
            template =  self.env['mail.template'].browse(template_id)
            template.send_mail(req.id,force_send=True)
        
