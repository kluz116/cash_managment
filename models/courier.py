from odoo import models, fields, api
from datetime import datetime

class Courier(models.Model):
    _name = "cash_managment.courier"
    _description = "This model is for courier services"
    _rec_name ="courier_name"

    
    courier_name = fields.Char(string="Courier ", required=True)
    email = fields.Char(string="Email ", required=True)
   