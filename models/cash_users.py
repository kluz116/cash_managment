from odoo import models, fields, api
from datetime import datetime

class res_users(models.Model):
    _inherit = 'res.partner'
    
    
    role = fields.Selection([('manager', 'Manager'), ('accountant', 'Accountant'),('cash_center', 'Cash Center')], string="Role",required=True)
    manager = fields.Many2one('res.partner',string ='Manager')
    branch_id = fields.Many2one('cash_managment.branch',string ='Branch', required=True)


