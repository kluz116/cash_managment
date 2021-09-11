from odoo import models, fields, api
from datetime import datetime

class CashBankRequest(models.Model):
    _name = "cash_managment.cash_bank_request"
    _description = "All Cash Center Requuests"
    _rec_name ="amount"

    currency_id = fields.Many2one('res.currency', string='Currency')
    amount = fields.Monetary(string='Amount', required=True)
    
    branch_id = fields.Many2one('cash_managment.branch',string ='From')
    from_bank= fields.Many2one('cash_managment.bank',string ='From Bank')
    to_branch = fields.Many2one('cash_managment.branch',string ='To', required=True)
    to_by = fields.Many2one('res.partner','Accountant',domain="[('branch_id', '=', to_branch)]")
    to_by_two = fields.Many2one('res.partner','Manager',domain="[('branch_id', '=', to_branch)]")
    courier = fields.Many2one('cash_managment.courier',ondelete='cascade',string='Courier')
    initiate_date =  fields.Datetime(string='Initiate Date', default=datetime.today())
    initiated_by = fields.Many2one('res.users','Initated By',default=lambda self: self.env.user)
    state = fields.Selection([('ongoing', 'Ongoing'),('closed', 'Closed')],default="ongoing", string="Status")

    

    @api.onchange ('to_branch')
    def on_change_toid(self):
        for record in self:
            self.to_by == record.to_by    
   