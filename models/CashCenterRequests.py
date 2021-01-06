from odoo import models, fields, api
from datetime import datetime

class CashCenterRequest(models.Model):
    _name = "cash_managment.cash_center_request"
    _description = "All Cash Center Requuests"
    _rec_name ="amount"

    branch_id = fields.Many2one('cash_managment.branch',string ='From', required=True)
    from_by = fields.Many2one('res.partner','Accountant',domain="[('branch_id', '=', branch_id)]")
    from_by_two = fields.Many2one('res.partner','Manager',domain="[('branch_id', '=', branch_id)]")
    to_branch = fields.Many2one('cash_managment.branch',string ='To', required=True)
    to_by = fields.Many2one('res.partner','Accountant',domain="[('branch_id', '=', to_branch)]")
    to_by_two = fields.Many2one('res.partner','Manager',domain="[('branch_id', '=', to_branch)]")
    courier = fields.Many2one('cash_managment.courier',ondelete='cascade',string='Courier')
    initiate_date =  fields.Datetime(string='Initiate Date', default=datetime.today())
    initiated_by = fields.Many2one('res.users','Initated By',default=lambda self: self.env.user)
    state = fields.Selection([('ongoing', 'Ongoing'),('closed', 'Closed')],default="ongoing", string="Status")
    amount = fields.Integer(string='Amount', required=True)
    
    @api.onchange ('branch_id')
    def on_change_fromid(self):
        for record in self:
            self.from_by == record.from_by

    @api.onchange ('to_branch')
    def on_change_toid(self):
        for record in self:
            self.to_by == record.to_by    
   