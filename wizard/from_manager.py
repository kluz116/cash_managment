from odoo import api, fields, models
from datetime import datetime

class FromManger(models.TransientModel):
    _name = "cash_managment.from_manager"
    _description = "From Manager Confirm"
    _rec_name = 'state'

    
    state = fields.Selection([('ongoing', 'Ongoing'),('confirmed_one', 'Confirmed'),('confirmed_two', 'Confirmed'),('confirmed_three', 'Confirmed')],default="ongoing", string="Status")
    from_manager_comment = fields.Text(string="Comment")
    from_manager_date =  fields.Datetime(string='Date', default=datetime.today())
   
    
    @api.multi
    def cash_confirm(self):
        self.write({'state': 'confirmed_one'})
        cash = self.env['cash_managment.request_confirmation'].browse(self._context.get('active_ids'))
        for req in cash:
            req.state = self.state
            req.from_manager_comment = self.from_manager_comment
            req.from_manager_date = self.from_manager_date
         
