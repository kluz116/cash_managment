from odoo import api, fields, models
from datetime import datetime

class DisregardRequest(models.TransientModel):
    _name = "cash_managment.disregard_request"
    _description = "Disregard Cash Request"
    _rec_name = 'disregard_date'

    
    state = fields.Selection([('ongoing', 'Ongoing'), ('pending', 'Pending'),('disregard','Disregarded'),('closed', 'Closed')],default="disregard", string="Status")
    disregard_comment= fields.Text(string="Comment")
    disregard_date =  fields.Datetime(string='Disregard Date', default=datetime.today())
    disregard_by = fields.Many2one('res.users','Disregared By By',default=lambda self: self.env.user)
    

    @api.multi
    def cash_disregard_xxx(self):
        #self.write({'state': 'disregard'})

        cash = self.env['cash_managment.request'].browse(self._context.get('active_ids'))
        for req in cash:
            req.state ='approve'
            
            cash = self.env['cash_managment.requestapproved'].search([('title', '=', req.id)])
            for req in cash:
                req.disregard_comment = self.disregard_comment
                req.disregard_date = self.disregard_date
                req.disregard_by = self.disregard_by
                req.state = 'disregard'
              
        #cashs = self.env['cash_managment.request'].browse(self._context.get('active_ids'))
        #for reqs in cashs:
            #reqs.state = 'approve'

            #template_id = self.env.ref('cash_managment.email_template_reject_request').id
            #template =  self.env['mail.template'].browse(template_id)
            #template.send_mail(req.id,force_send=True)
        
