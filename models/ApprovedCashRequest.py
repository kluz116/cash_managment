from odoo import models, fields, api
from datetime import datetime

class ApprovedCashRequest(models.Model):
    _name = "cash_managment.requestapproved"
    _description = "Request Approved Model"
    _rec_name ="amount_available"

    
    branch_id = fields.Many2one('cash_managment.branch',string ='From', required=True)
    from_by = fields.Many2one('res.partner','Accountant',domain="[('branch_id', '=', branch_id)]")
    from_by_two = fields.Many2one('res.partner','Manager',domain="[('branch_id', '=', branch_id)]")
    to_branch = fields.Many2one('cash_managment.branch',string ='To', required=True)
    to_by = fields.Many2one('res.partner','Accountant',domain="[('branch_id', '=', to_branch)]")
    to_by_two = fields.Many2one('res.partner','Manager',domain="[('branch_id', '=', to_branch)]")
    courier = fields.Many2one('cash_managment.courier',ondelete='cascade',string='Courier')
    initiate_date =  fields.Datetime(string='Initiate Date', default=datetime.today())
    initiated_by = fields.Many2one('res.users','Initated By',default=lambda self: self.env.user)
    state = fields.Selection([('ongoing', 'Ongoing'), ('pending', 'Pending'),('disregard','Disregarded'),('closed', 'Closed')],default="ongoing", string="Request Status")
    title = fields.Many2one('cash_managment.request',string='Requested', required=True, domain = [('state','=','approve')])
    from_by_branch = fields.Integer(compute='_compute_from_by',string='From',store=True)
    currency_id = fields.Many2one('res.currency', string='Currency',required=True)
    amount_available = fields.Monetary(string='Amount Available', required=True)
    cash_date =  fields.Datetime(string='Cash Transfer Date', default=datetime.today())
    ref_request = fields.Char(related ='title.unique_field', string='Ref',store=True)
    disregard_comment =  fields.Text(string='Comment')
    disregard_date =  fields.Datetime(string='Disregarded Date', default=datetime.today())
    disregard_by = fields.Many2one('res.users','Disregarded By')
    
    @api.onchange ('branch_id')
    def on_change_fromid(self):
        for record in self:
            self.from_by == record.from_by

    @api.onchange ('to_branch')
    def on_change_toid(self):
        for record in self:
            self.to_by == record.to_by    

    
    @api.depends('from_by')
    def _compute_from_by(self):
        for record in self:
            record.from_by_branch = record.from_by.id


    @api.model
    def _update_notified_initiated(self):
        initiated_req = self.env['cash_managment.requestapproved'].search([('state', '=', 'pending')])
        for request in initiated_req:
            template_id = self.env.ref('cash_managment.email_template_initiate_request').id
            template =  self.env['mail.template'].browse(template_id)
            template.send_mail(request.id,force_send=True)
 
