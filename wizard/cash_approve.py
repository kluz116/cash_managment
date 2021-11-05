from odoo import api, fields, models
from datetime import datetime

class CashApprove(models.TransientModel):
    _name = "cash_managment.approve_cash"
    _description = "Approve Cash"
    _rec_name = 'approval_comment'

    
    
    state =  fields.Selection([('new','New'),('validate','Validate'),('reject','Reject'),('approve','Approve'),('closed','Closed'),('implement','Implement')],string="Status", required=True, default="new")
    approval_comment = fields.Text(string="Comment")
    approval_date =  fields.Datetime(string='Approval Date', default=datetime.today())
    approved_by = fields.Many2one('res.users','Approved By',default=lambda self: self.env.user)
    hod_expire_status =  fields.Selection([('yes','Yes'),('no','No')],string="Expire Status", required=True, default="no")

    @api.multi
    def cash_approve(self):
        self.write({'state': 'approve'})
        cash = self.env['cash_managment.request'].browse(self._context.get('active_ids'))
        for req in cash:
            req.state = self.state
            req.approval_comment = self.approval_comment
            req.approval_date = self.approval_date
            req.approved_by = self.approved_by
            req.hod_expire_status = self.hod_expire_status

            template_id = self.env.ref('cash_managment.email_template_approve_request').id
            template =  self.env['mail.template'].browse(template_id)
            template.send_mail(req.id,force_send=True)
            
        
