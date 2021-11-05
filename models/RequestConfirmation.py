from odoo import models, fields, api,exceptions
from datetime import datetime

class Re(models.Model):
    _name = "cash_managment.request_confirmation"
    _description = "This is a model for all requests confirmations"
    _rec_name ="total"


    partner_ids = fields.Many2one ('res.partner', 'Customer', default = lambda self: self.env.user.partner_id.id )
    from_bys = fields.Integer(compute='_compute_branch_from_bys',string='From',store=True)
    partner_id = fields.Many2one('res.users', string='User', track_visibility='onchange', readonly=True, default=lambda self: self.env.user.partner_id.id)
    total = fields.Float(compute='_compute_total',string="Total",store=True)
    total_usd = fields.Float(compute='_compute_total_dollars',string="Total USD",store=True)
    #from_m =  fields.Integer(related ='initiated_request_id.from_by.id', string='To',store=True)
    initiated_request_id = fields.Many2one('cash_managment.requestapproved',string='Expected Amount Transfered',required=True)
    #initiated_request_id = fields.Many2one('cash_managment.requestapproved',string='Expected Amount Transfered', domain = [('state','=','pending')],required=True)
         
    currency_id = fields.Many2one('res.currency', string='Currency')
    actual_amount = fields.Monetary(string="Actual Amount Transfered", required=True)
    from_branch = fields.Integer(related ='initiated_request_id.branch_id.branch_code', string='From', store=True)
    to_branch = fields.Integer(related ='initiated_request_id.to_branch.branch_code', string='To',store=True)
    deno_fifty_thounsand = fields.Monetary(string="50,000 Shs")
    deno_twenty_thounsand = fields.Monetary(string="20,000 Shs")
    deno_ten_thounsand = fields.Monetary(string="10,000 Shs")
    deno_five_thounsand = fields.Monetary(string="5,000 Shs")
    deno_two_thounsand = fields.Monetary(string="2,000 Shs")
    deno_one_thounsand = fields.Monetary(string="1,000 Shs")
    coin_one_thounsand = fields.Monetary(string="1,000 Shs")
    coin_five_houndred = fields.Monetary(string="500 Shs")
    coin_two_hundred = fields.Monetary(string="200 Shs")
    coin_one_hundred = fields.Monetary(string="100 Shs")
    coin_fifty = fields.Monetary(string="50 Shs")
    hundred_dollar = fields.Monetary(string="$100")
    fifty_dollar = fields.Monetary(string="$50")
    twenty_dollar = fields.Monetary(string="$20")
    ten_dollar = fields.Monetary(string="$10")
    five_dollar = fields.Monetary(string="$5")
    one_dollar = fields.Monetary(string="$1")
    confirm_date =  fields.Datetime(string='Confirmed Date', default=datetime.today())
    state = fields.Selection([('ongoing', 'Pending Manager Approval'),('confirmed_one', 'Pending Accountant Approval'),('confirmed_two', 'Pending Manager Approval'),('confirmed_three', 'Confirmed')],default="ongoing", string="Status")
    from_manager_comment = fields.Text(string="Comment")
    from_manager_date =  fields.Datetime(string='Date', default=datetime.today())
    to_manager_comment = fields.Text(string="Comment")
    to_manager_date =  fields.Datetime(string='Date', default=datetime.today())
    confirmed_by = fields.Many2one('res.users','Confirmed By:',default=lambda self: self.env.user)
    user_id = fields.Many2one('res.users', string='User', track_visibility='onchange', readonly=True, default=lambda self: self.env.user.id)
    from_manager =  fields.Integer(related ='initiated_request_id.from_by_two.id', string='To',store=True)
    to_branch_accountant =  fields.Integer(related ='initiated_request_id.to_by.id', string='To',store=True)
    to_branch_manager =  fields.Integer(related ='initiated_request_id.to_by_two.id', string='To',store=True)
    current_user = fields.Boolean('is current user ?', compute='_get_current_user')
    current_to_branch_accountant = fields.Boolean('is current user ?', compute='_get_to_branch_accountant')
    current_to_branch_manager = fields.Boolean('is current user ?', compute='_get_to_branch_manager')
     
   


    @api.depends('from_manager')
    def _get_current_user(self):
        for e in self:
            partner = self.env['res.users'].browse(self.env.uid).partner_id
            e.current_user = (True if partner.id == self.from_manager else False)

    @api.depends('to_branch_accountant')
    def _get_to_branch_accountant(self):
        for e in self:
            partner = self.env['res.users'].browse(self.env.uid).partner_id
            e.current_to_branch_accountant = (True if partner.id == self.to_branch_accountant else False)
 

    @api.depends('to_branch_manager')
    def _get_to_branch_manager(self):
        for e in self:
            partner = self.env['res.users'].browse(self.env.uid).partner_id
            e.current_to_branch_manager = (True if partner.id == self.to_branch_manager else False)
 
    
    @api.one
    @api.constrains('total','actual_amount')
    def _check_amount(self):
        if self.actual_amount != self.total:
            raise exceptions.ValidationError("The Total Amount {total} Shs Does Not Equal {amount} Shs The Actual Amount Expected To Be Transfered".format(total=self.total,amount = self.actual_amount))

    
    @api.depends('deno_fifty_thounsand', 'deno_twenty_thounsand','deno_ten_thounsand','deno_five_thounsand','deno_two_thounsand','deno_one_thounsand','coin_one_thounsand','coin_five_houndred','coin_two_hundred','coin_one_hundred','coin_fifty')
    def _compute_total(self):
        for record in self:
            record.total = record.deno_fifty_thounsand + record.deno_twenty_thounsand + record.deno_ten_thounsand + record.deno_five_thounsand + record.deno_two_thounsand + record.deno_one_thounsand + record.coin_one_thounsand + record.coin_five_houndred + record.coin_two_hundred + record.coin_one_hundred + record.coin_fifty

    @api.depends('hundred_dollar','fifty_dollar','twenty_dollar','ten_dollar','five_dollar','one_dollar')
    def _compute_total_dollars(self):
        for rec in self:
            rec.total_usd = rec.hundred_dollar + rec.fifty_dollar + rec.twenty_dollar + rec.ten_dollar + rec.five_dollar + rec.one_dollar

    @api.depends('partner_ids')
    def _compute_branch_from_bys(self):
        for record in self:
            record.from_bys = record.partner_ids.id

   