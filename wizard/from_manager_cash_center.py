from odoo import api, fields, models
from datetime import datetime

class FromMangerCashCenter(models.TransientModel):
    _name = "cash_managment.from_manager_cash_center"
    _description = "From Manager Confirm"
    _rec_name = 'state'

    
    state = fields.Selection([('ongoing', 'Pending Manager Approval'),('confirmed_one', 'Pending Accountant Approval'),('confirmed_two', 'Pending Manager Approval'),('confirmed_three', 'Confirmed')], string="Status")
    from_manager_comment = fields.Text(string="Comment")
    from_manager_date =  fields.Datetime(string='Date', default=datetime.today())
   
    
    @api.multi
    def cash_confirm_cash_center(self):
        self.write({'state': 'confirmed_one'})
        cash = self.env['cash_managment.cash_center_request_confirmation'].browse(self._context.get('active_ids'))
        for req in cash:
            req.state = self.state
            req.from_manager_comment = self.from_manager_comment
            req.from_manager_date = self.from_manager_date
         
