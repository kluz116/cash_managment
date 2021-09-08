from odoo import models, fields, api
from datetime import datetime

class Bank(models.Model):
    _name = "cash_managment.bank"
    _description = "This is a model for other institutions"
    _rec_name ="bank_name"

    bank_name = fields.Char(string="Bank Name", required=True)

  
    
   