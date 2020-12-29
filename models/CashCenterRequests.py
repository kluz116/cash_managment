from odoo import models, fields, api
from datetime import datetime

class CashCenterRequest(models.Model):
    _name = "cash_managment.cash_center_request"
    _description = "All Cash Center Requuests"
    _rec_name ="amount"

    from_branch = fields.Many2one('cash_managment.branch',string ='From Branch', required=True)
    to_branch = fields.Many2one('cash_managment.branch',string ='To Branch', required=True)
    courier = fields.Many2one('cash_managment.courier',ondelete='cascade',string='Courier')
    initiate_date =  fields.Datetime(string='Initiate Date', default=datetime.today())
    initiated_by = fields.Many2one('res.users','Initated By',default=lambda self: self.env.user)
    state = fields.Selection([('ongoing', 'Ongoing'), ('pending', 'Pending'),('confirmed', 'Confirmed')],default="ongoing", string="Request Status")
    amount = fields.Integer(string='Amount', required=True)
    