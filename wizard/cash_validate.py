from odoo import api, fields, models
from datetime import datetime

class ValidateCash(models.TransientModel):
    _name = "cash_managment.validate_cash"
    _description = "Validate Cash"
    _rec_name = 'validate_comment'

    state =  fields.Selection([('new','New'),('validate','Validated'),('reject','Reject'),('approve','Approve'),('closed','Closed'),('implement','Implement')],string="Status", required=True, default="new")
    validate_comment = fields.Text(string="Comment")
    validate_date =  fields.Datetime(string='Validate Date', default=datetime.today())
    validated_by = fields.Many2one('res.users','Validated By',default=lambda self: self.env.user)

 

    @api.multi
    def action_validate_cash(self):
        self.write({'state': 'validate'})
        cash = self.env['cash_managment.request'].browse(self._context.get('active_ids'))
        for req in cash:
            req.state = self.state
            req.validate_comment = self.validate_comment
            req.validate_date = self.validate_date
            req.validated_by = self.validated_by
        
            template_id = self.env.ref('cash_managment.email_template_validate_request').id
            template =  self.env['mail.template'].browse(template_id)
            template.send_mail(req.id,force_send=True)
            
            
        
