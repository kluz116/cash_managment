from odoo import models, fields, api
from datetime import datetime


class CashManagment(models.Model):
    _name = "cash_managment.request"
    _description ="Cash Requests Model"
    _rec_name ='title'

    title = fields.Integer(string='Request Amount', required=True)
    description  = fields.Text(string="Description", required=True, size=50)
    state =  fields.Selection([('new','New'),('validate','Validated'),('cancel','Canceled'),('reject','Reject'),('approve','Approved'),('closed','Closed'),('initiated','Initiated')],string="Status", required=True, default="new")
    start_date = fields.Datetime(string='Start Date', default=datetime.now())
    end_date = fields.Datetime(string='Start Date')
    close_date = fields.Datetime(string='Close Date')
    validate_comment = fields.Text(string="Comment")
    validate_date =  fields.Datetime(string='Validate Date')
    validated_by = fields.Many2one('res.users',String='Validated By')
    approval_comment = fields.Text(string="Comment")
    approval_date =  fields.Datetime(string='Approval Date')
    cancel_comment = fields.Text(string="Comment")
    cancel_date =  fields.Datetime(string='Cancel Date')
    canceled_by = fields.Many2one('res.users',string ='Canceled By')
    supervision_comment = fields.Text(string="Comment")
    supervision_date =  fields.Datetime(string='Cancel Date')
    supervised_by = fields.Many2one('res.users',string ='Supervised By')
    approved_by = fields.Many2one('res.users',string="Approved By")
    created_by = fields.Many2one('res.users',string ='Created By',default=lambda self: self.env.user)
    reject_comment = fields.Text(string="Reject Comment")
    reject_date =  fields.Datetime(string='Reject Date', default=datetime.now())
    rejected_by = fields.Many2one('res.users','Canceled By')
    branch_code_to = fields.Integer(compute='_compute_branch',string='Branch Code',store=True)
    branch_code_from = fields.Integer(string='Branch Code To')
    branch_manager_to = fields.Integer(compute='_compute_manager',string='Manager',store=True)
    branch_accountant_from = fields.Integer(string='From Branch Accountatnt')
    branch_manager_from = fields.Integer(string='From Branch Manager')
    user_id = fields.Many2one('res.users', string='User', track_visibility='onchange', readonly=True, default=lambda self: self.env.user.id)
    partner_id = fields.Many2one ('res.partner', 'Customer', default = lambda self: self.env.user.partner_id )
    

    @api.depends('user_id')
    def _compute_branch(self):
        for record in self:
            record.branch_code_to = record.user_id.branch_id.branch_code

    @api.depends('user_id')
    def _compute_manager(self):
        for record in self:
            record.branch_manager_to = record.partner_id.manager




   


    
  