from odoo import models, fields, api
from datetime import datetime

class ApprovedCashRequest(models.Model):
    _name = "cash_managment.requestapproved"
    _description = "Request Approved Model"
    _rec_name ="title"

    
    branch_id = fields.Many2one('cash_managment.branch',string ='From', required=True)
    from_by = fields.Many2one('res.partner','Name',domain="[('branch_id', '=', branch_id)]")
    to_branch = fields.Many2one('cash_managment.branch',string ='To', required=True)
    to_by = fields.Many2one('res.partner','Name',domain="[('branch_id', '=', to_branch)]")
    courier = fields.Many2one('cash_managment.courier',ondelete='cascade',string='Courier')
    initiate_date =  fields.Datetime(string='Initiate Date', default=datetime.today())
    initiated_by = fields.Many2one('res.users','Initated By',default=lambda self: self.env.user)
    state = fields.Selection([('ongoing', 'Ongoing'), ('pending', 'Pending'),('closed', 'Closed')],default="ongoing", string="Request Status")
    title = fields.Many2one('cash_managment.request',string='Requested Amount', required=True, domain = [('state','=','approve')])
    current_user = fields.Boolean('is current user ?', compute='_get_current_user')

    @api.depends('to_by')
    def _get_current_user(self):
        for e in self:
            partner = self.env['res.users'].browse(self.env.uid).partner_id
            e.current_user = (True if partner.id == self.to_by.id else False)
    @api.onchange ('branch_id')
    def on_change_fromid(self):
        for record in self:
            self.from_by == record.from_by

    @api.onchange ('to_branch')
    def on_change_toid(self):
        for record in self:
            self.to_by == record.to_by    
   
