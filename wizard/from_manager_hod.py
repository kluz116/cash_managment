from odoo import api, fields, models
from datetime import datetime

class FromMangerHod(models.TransientModel):
    _name = "cash_managment.from_manager_hod"
    _description = "From Manager Confirm"
    _rec_name = 'state'

    
    
    state = fields.Selection([('ongoing', 'Pending Manager Confirmation From'),('reject_one','Rejected'),('confirmed_three', 'Confirmed')],default="ongoing", string="Status")
    from_manager_comment = fields.Text(string="Comment")
    from_manager_date =  fields.Datetime(string='Date', default=lambda self: fields.datetime.now())
   
    
    @api.multi
    def cash_confirm_hod(self):
        self.write({'state': 'confirmed_three'})
        cash = self.env['cash_managment.request_confirmation_bank_hod'].browse(self._context.get('active_ids'))
        for req in cash:
            req.state = self.state
            req.from_manager_comment = self.from_manager_comment
            req.from_manager_date = self.from_manager_date
            req.initiated_request_id.state = 'closed'

            template_id = self.env.ref('cash_managment.email_template_from_accountant_confirm_hod_final').id
            template =  self.env['mail.template'].browse(template_id)
            template.send_mail(req.id,force_send=True)
        


         
