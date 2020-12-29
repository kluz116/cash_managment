from odoo import api, fields, models
from datetime import datetime

class CashCenterToConfirmCash(models.Model):
    _name = "cash_managment.confirm_cash_centerto"
    _description = "Confirm Cash"
    _rec_name = 'amount_request_id'

    
    total = fields.Float(compute='_compute_total',string="Total")
    amount_request_id = fields.Many2one('cash_managment.cash_center_request_confirmation',string='Amount To Confirm.')
    #to_branch = fields.Char(related ='amount_request_id.to_branch', string='To')
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
    confirm_date =  fields.Datetime(string='Confirmed Date', default=datetime.today())
    state = fields.Selection([('ongoing', 'Ongoing'), ('pending', 'Pending'),('confirmed', 'Confirmed')],default="ongoing", string="Status")
    #confirmed_by = fields.Many2one('res.users','Confirmed By:',default=lambda self: self.env.user)
    confirmed_by = fields.Many2one('res.users', string='Confirmed By', track_visibility='onchange', readonly=True, states={'draft': [('readonly', False)]}, default=lambda self: self.env.user.id)
    user_id = fields.Many2one('res.users', string='Confirmed By', track_visibility='onchange', readonly=True, states={'draft': [('readonly', False)]}, default=lambda self: self.env.user.id)
    
  

    @api.depends('deno_fifty_thounsand', 'deno_twenty_thounsand','deno_ten_thounsand','deno_five_thounsand','deno_two_thounsand','deno_one_thounsand','coin_one_thounsand','coin_five_houndred','coin_two_hundred','coin_one_hundred','coin_fifty')
    def _compute_total(self):
        for record in self:
            record.total = record.deno_fifty_thounsand + record.deno_twenty_thounsand + record.deno_ten_thounsand + record.deno_five_thounsand + record.deno_two_thounsand + record.deno_one_thounsand + record.coin_one_thounsand + record.coin_five_houndred + record.coin_two_hundred + record.coin_one_hundred + record.coin_fifty

    