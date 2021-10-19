from odoo import models, fields, api
from datetime import datetime

class ApprovedCashRequestAmount(models.Model):
    _name ='cash_managment.approved_amount_request'
    _rec_name ='amount'

    currency_id = fields.Many2one('res.currency', string='Currency')
    #title = fields.Monetary(string='Amount', required=True)

    request_id = fields.Many2one('cash_managment.request',string='')
    amount = fields.Monetary(related = "request_id.title" ,store=True) 
    branch_code_to = fields.Integer(related = "request_id.branch_code_to" ,store=True) 
    start_date = fields.Datetime(related = "request_id.start_date", store=True) 

    