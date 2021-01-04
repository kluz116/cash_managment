from odoo import models, fields, api,exceptions
from datetime import datetime

class Re(models.Model):
    _name = "cash_managment.request_confirmation"
    _description = "This is a model for all requests confirmations"
    _rec_name ="total"

    total = fields.Float(compute='_compute_total',string="Total",store=True)
    total_usd = fields.Float(compute='_compute_total_dollars',string="Total USD",store=True)
    initiated_request_id = fields.Many2one('cash_managment.requestapproved',string='Expected Amount To Confirm', domain = [('state','=','pending')])
    actual_amount = fields.Integer(string="Actual Amount Corfimed")
    from_branch = fields.Integer(related ='initiated_request_id.branch_id.branch_code', string='From', store=True)
    to_branch = fields.Integer(related ='initiated_request_id.to_branch.branch_code', string='To',store=True)
    deno_fifty_thounsand = fields.Integer(string="50,000 Shs")
    deno_twenty_thounsand = fields.Integer(string="20,000 Shs")
    deno_ten_thounsand = fields.Integer(string="10,000 Shs")
    deno_five_thounsand = fields.Integer(string="5,000 Shs")
    deno_two_thounsand = fields.Integer(string="2,000 Shs")
    deno_one_thounsand = fields.Integer(string="1,000 Shs")
    coin_one_thounsand = fields.Integer(string="1,000 Shs")
    coin_five_houndred = fields.Integer(string="500 Shs")
    coin_two_hundred = fields.Integer(string="200 Shs")
    coin_one_hundred = fields.Integer(string="100 Shs")
    coin_fifty = fields.Integer(string="50 Shs")
    hundred_dollar = fields.Integer(string="$100")
    fifty_dollar = fields.Integer(string="$50")
    twenty_dollar = fields.Integer(string="$20")
    ten_dollar = fields.Integer(string="$10")
    five_dollar = fields.Integer(string="$5")
    one_dollar = fields.Integer(string="$1")
    confirm_date =  fields.Datetime(string='Confirmed Date', default=datetime.today())
    state = fields.Selection([('ongoing', 'Ongoing'),('confirmed_one', 'Confirmed'),('confirmed_two', 'Confirmed'),('confirmed_three', 'Confirmed')],default="ongoing", string="Status")
    confirmed_by = fields.Many2one('res.users','Confirmed By:',default=lambda self: self.env.user)
    user_id = fields.Many2one('res.users', string='User', track_visibility='onchange', readonly=True, default=lambda self: self.env.user.id)
    to_users =  fields.Integer(related ='initiated_request_id.to_by.id', string='To',store=True)
    #user_id = fields.Many2one('res.partner','Customer', default=lambda self: self.env.user.partner_id)
    #current_user_id =  fields.Integer(related ='current_user.id', string='Current User Id')
    #user_id = fields.Many2one('res.users', 'User', related='resource_id.user_id')
    current_user = fields.Boolean('is current user ?', compute='_get_current_user')

    @api.depends('to_users')
    def _get_current_user(self):
        for e in self:
            partner = self.env['res.users'].browse(self.env.uid).partner_id
            e.current_user = (True if partner.id == self.to_users else False)
 
    '''
    @api.one
    @api.constrains('total','initiated_request_id')
    def _check_amount(self):
        if self.initiated_request_id.title.title != self.total:
            raise exceptions.ValidationError("The Amount {total} Shs Does Not Equal {amount} Shs  Which Was Approved By Cash Center".format(total=self.total,amount = self.initiated_request_id.title.title))

    '''
    @api.depends('deno_fifty_thounsand', 'deno_twenty_thounsand','deno_ten_thounsand','deno_five_thounsand','deno_two_thounsand','deno_one_thounsand','coin_one_thounsand','coin_five_houndred','coin_two_hundred','coin_one_hundred','coin_fifty')
    def _compute_total(self):
        for record in self:
            record.total = record.deno_fifty_thounsand + record.deno_twenty_thounsand + record.deno_ten_thounsand + record.deno_five_thounsand + record.deno_two_thounsand + record.deno_one_thounsand + record.coin_one_thounsand + record.coin_five_houndred + record.coin_two_hundred + record.coin_one_hundred + record.coin_fifty

    @api.depends('hundred_dollar','fifty_dollar','twenty_dollar','ten_dollar','five_dollar','one_dollar')
    def _compute_total_dollars(self):
        for rec in self:
            rec.total_usd = rec.hundred_dollar + rec.fifty_dollar + rec.twenty_dollar + rec.ten_dollar + rec.five_dollar + rec.one_dollar

    @api.depends('current_user')
    def _get_partner(self):
        partner = self.env['res.users'].browse(self.env.uid).partner_id
        for rec in self: 
            rec.current_user = partner.id