from odoo import api, fields, models
from datetime import datetime

class CashBankingSupervision(models.TransientModel):
    _name = "cash_managment.supervise_cash_banking"
    _description = "Supervise Cash Request"
    _rec_name = 'state'

    state = fields.Selection([('New', 'New'),('reject_one','Rejected'),('reject_two','Rejected'),('approved','Approved'),('initiated','Initiated'),('confirm', 'Confirmed'),('expired_branch','Expired'),('expired_hod','Expired')],default="approved", string="Status")
    supervision_comment = fields.Text(string="Comment")
    supervision_date =  fields.Datetime(string='Date', default=lambda self: fields.datetime.now())
    supervised_by = fields.Many2one('res.users','Canceled By',default=lambda self: self.env.user)
    cash_date =  fields.Datetime(string='Effective Date', default=lambda self: fields.datetime.now())
    courier = fields.Many2one('cash_managment.courier',ondelete='cascade',string='Courier')
    
    @api.multi
    def cash_banking_supervision(self):
        self.write({'state': 'initiated'})
        cash = self.env['cash_managment.cash_branch_bank_request'].browse(self._context.get('active_ids'))
        for req in cash:
            req.state = self.state
            req.supervision_comment = self.supervision_comment
            req.supervision_date = self.supervision_date
            req.supervised_by = self.supervised_by
            req.cash_date = self.cash_date
            req.courier = self.courier

            template_id = self.env.ref('cash_managment.email_template_branch_bank_request_final').id
            template =  self.env['mail.template'].browse(template_id)
            template.send_mail(req.id,force_send=True)



        
