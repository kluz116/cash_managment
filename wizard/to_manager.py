from odoo import api, fields, models
from datetime import datetime

class ToManger(models.TransientModel):
    _name = "cash_managment.to_manager"
    _description = "To Manager Confirm"
    _rec_name = 'state'


    state = fields.Selection([('ongoing', 'Pending Manager'),('confirmed_one', 'Pending Accountant'),('confirmed_two', 'Pending Manager'),('confirmed_three', 'Confirmed')],default="confirmed_two", string="Status")
    to_manager_comment = fields.Text(string="Comment")
    to_manager_date =  fields.Datetime(string='Date', default=lambda self: fields.datetime.now())
   
    
    @api.multi
    def cash_confirm_manager(self):
        self.write({'state': 'confirmed_three'})
        cash = self.env['cash_managment.request_confirmation'].browse(self._context.get('active_ids'))
        for req in cash:
            req.state = self.state
            req.to_manager_comment = self.to_manager_comment
            req.to_manager_date = self.to_manager_date
            req.initiated_request_id.state = 'closed'
            req.initiated_request_id.title.state = 'closed'

            template_id = self.env.ref('cash_managment.email_template_final_manager_confirm').id
            template =  self.env['mail.template'].browse(template_id)
            template.send_mail(req.id,force_send=True)
        
           
        #cash = self.env['cash_managment.requestapproved'].browse(self._context.get('active_ids'))
        #for req in res:
            #req.initiated_request_id.state = 'Pending'

           # window_coverage = self.env['cash_managment.coveragewindow'].search([('working_days', '=', self.week_day)])


        
         
