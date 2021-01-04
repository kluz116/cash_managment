from odoo import models, fields, api
from datetime import datetime

class ApprovedCashRequest(models.TransientModel):
    _name = "cash_managment.approved_request"
    _description = "this shows all agents that get mapped to tickets"
    _rec_name ="title"


    branch_id = fields.Many2one('cash_managment.branch',string ='From Branch', required=True)
    from_branch_id = fields.Integer(related='branch_id.id')
    from_by = fields.Many2one('res.partner','Accountant',domain="[('branch_id', '=', branch_id)]")
    from_by_two = fields.Many2one('res.partner','Manager',domain="[('branch_id', '=', branch_id)]")
    from_by_id = fields.Integer(related='from_by.id')
    from_by_id_two = fields.Integer(related='from_by_two.id')
    to_branch = fields.Many2one('cash_managment.branch',string ='To Branch', required=True)
    to_by = fields.Many2one('res.partner','Accountant',domain="[('branch_id', '=', to_branch)]")
    to_by_two = fields.Many2one('res.partner','Manager',domain="[('branch_id', '=', to_branch)]")
    to_by_id = fields.Integer(related='to_by.id')
    to_by_id_two = fields.Integer(related='to_by_two.id')
    to_branch_id = fields.Integer(related='to_branch.id')
    courier = fields.Many2one('cash_managment.courier',ondelete='cascade',string='Courier')
    courier_id = fields.Integer(related='courier.id',string="Courier")
    initiate_date =  fields.Datetime(string='Initiate Date', default=datetime.today())
    initiated_by = fields.Many2one('res.users','Initated By',default=lambda self: self.env.user)
    initiated_by_id = fields.Integer(related='initiated_by.id')
    state = fields.Selection([('ongoing', 'Ongoing'), ('pending', 'Pending'),('confirmed', 'Confirmed')],default="pending", string="Request Status")
    title = fields.Many2one('cash_managment.request',string='Request Amount', required=True, domain = [('state','=','approve')])
    title_id = fields.Integer(related='title.id')
    from_branch_request = fields.Integer(compute='_compute_branch_from', string='To')
   
   
    
    @api.onchange ('branch_id')
    def on_change_fromid(self):
        for record in self:
            self.from_by == record.from_by

    @api.onchange ('to_branch')
    def on_change_toid(self):
        for record in self:
            self.to_by == record.to_by    
    
    @api.depends('branch_id')
    def _compute_branch_from(self):
        for record in self:
            record.from_branch_request = record.branch_id.branch_code

    @api.depends('to_branch')
    def _compute_branch_manager_to(self):
        for record in self:
            record.from_branch_request = record.title.branch_manager_to
    

    @api.multi
    def initiate_request(self):
        #self.write({'state': 'pending'})  
        vals = {'branch_id': self.from_branch_id,
                'from_by': self.from_by_id,
                'from_by_two': self.from_by_id_two,
                 'to_branch': self.to_branch_id,
                 'to_by': self.to_by_id,
                 'to_by': self.to_by_id_two,
                 'courier':self.courier_id,
                 'initiate_date':self.initiate_date,
                 'initiated_by':self.initiated_by_id,
                 'state':self.state,
                 'title':self.title_id}

        self.env['cash_managment.requestapproved'].create(vals)
        cash_confirm_req = self.env['cash_managment.request'].browse(self._context.get('active_ids'))
        for request in cash_confirm_req:
            request.branch_code_from = self.from_branch_request
            request.branch_manager_from = self.from_by_id_two
            request.branch_accountant_from = self.from_by_id
            request.state = 'closed'

            # template_id = self.env.ref('cash_managment.email_template_initiate_request').id
            #template =  self.env['mail.template'].browse(template_id)
            #template.send_mail(request.id,force_send=True)
 
