from odoo import models, fields, api
from datetime import datetime

class res_users(models.Model):
    _inherit = 'res.partner'
    
    
    role = fields.Selection([('manager', 'Branch Manager'), ('accountant', 'Branch Accountant'),('cash_center', 'Cash Support Team'),('it_support', 'IT Support Team')], string="Role",required=True)
    manager = fields.Many2one('res.partner',string ='Manager')
    branch_id = fields.Many2one('cash_managment.branch',string ='Branch', required=True)


