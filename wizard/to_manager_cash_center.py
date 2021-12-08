from odoo import api, fields, models
from datetime import datetime

class ToMangerCashCenter(models.TransientModel):
    _name = "cash_managment.to_manager_cash_center"
    _description = "To Manager Confirm"
    _rec_name = 'state'

    
    state = fields.Selection([('ongoing', 'Pending Manager Approval'),('confirmed_one', 'Pending Accountant Approval'),('confirmed_two', 'Pending Manager Approval'),('confirmed_three', 'Confirmed')],default="confirmed_two", string="Status")
    to_manager_comment = fields.Text(string="Comment")
    to_manager_date =  fields.Datetime(string='Date', default=lambda self: fields.datetime.now())
   
    
    @api.multi
    def cash_confirm_manager_cashcenter(self):
        self.write({'state': 'confirmed_three'})
        cash = self.env['cash_managment.cash_center_request_confirmation'].browse(self._context.get('active_ids'))
        for req in cash:
            req.state = self.state
            req.to_manager_comment = self.to_manager_comment
            req.to_manager_date = self.to_manager_date
            req.initiated_request_id.state = 'closed'
            template_id = self.env.ref('cash_managment.email_template_to_manager_confirm_cash_center').id
            template =  self.env['mail.template'].browse(template_id)
            template.send_mail(req.id,force_send=True)
         


            
         
