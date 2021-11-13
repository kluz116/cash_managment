from odoo import models, fields, api
from datetime import datetime

class WindowHod(models.Model):
    _name = "cash_managment.coveragewindow_hod"
    _description = "Working Hours"
    _rec_name ="working_days"

    working_days = fields.Selection([('0', 'Monday'), ('1', 'Tuesday'), ('2', 'Wensday'), ('3', 'Thursday'),('4', 'Friday'),('5', 'Saturday'),('6', 'Sunday')], default="0", string="Working Days")
    from_hour = fields.Float('Working Hour From :')
    to_hour = fields.Float('Working Hour To : ')





    
   