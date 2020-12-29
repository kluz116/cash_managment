from odoo import models, fields, api
from datetime import datetime

class Branch(models.Model):
    _name = "cash_managment.branch"
    _description = "Branch Model"
    _rec_name ="branch_name"

    branch_name = fields.Char(string="Branch Name", required=True)
    branch_code = fields.Integer(string="Branch Code", required=True)
    user_id = fields.One2many('res.partner','branch_id', string="Name")
  
    
   