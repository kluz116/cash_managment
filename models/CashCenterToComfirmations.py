from odoo import api, fields, models
from datetime import datetime

class CashCenterToConfirmCash(models.Model):
    _name = "cash_managment.confirm_cash_centerto"
    _description = "Confirm Cash"
    _rec_name = 'amount_request_ids'

    
    total = fields.Float(compute='_compute_total',string="Total",store=True)
    total_usd = fields.Float(compute='_compute_total_dollars',string="Total USD",store=True)

    amount_request_ids = fields.Many2one('cash_managment.cash_center_request_confirmation',string='Expected Amount Transfered',domain = [('state','=','confirmed_one')],required=True)
    currency_id = fields.Many2one('res.currency', string='Currency')
    actual_amount = fields.Monetary(string="Actual Amount Transfered", required=True)
    to_branch = fields.Integer(related ='amount_request_ids.to_branch', string='To', store=True)
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
    state = fields.Selection([('ongoing', 'Ongoing'), ('pending', 'Pending'),('confirmed', 'Confirmed')],default="ongoing", string="Status")
    confirmed_by = fields.Many2one('res.users', string='Confirmed By', track_visibility='onchange', readonly=True, states={'draft': [('readonly', False)]}, default=lambda self: self.env.user.id)
    user_id = fields.Many2one('res.users', string='Confirmed By', track_visibility='onchange', readonly=True, default=lambda self: self.env.user.id)
    trx_proof = fields.Binary('Upload File')
  

    @api.depends('deno_fifty_thounsand', 'deno_twenty_thounsand','deno_ten_thounsand','deno_five_thounsand','deno_two_thounsand','deno_one_thounsand','coin_one_thounsand','coin_five_houndred','coin_two_hundred','coin_one_hundred','coin_fifty')
    def _compute_total(self):
        for record in self:
            record.total = record.deno_fifty_thounsand + record.deno_twenty_thounsand + record.deno_ten_thounsand + record.deno_five_thounsand + record.deno_two_thounsand + record.deno_one_thounsand + record.coin_one_thounsand + record.coin_five_houndred + record.coin_two_hundred + record.coin_one_hundred + record.coin_fifty

    

    @api.depends('hundred_dollar','fifty_dollar','twenty_dollar','ten_dollar','five_dollar','one_dollar')
    def _compute_total_dollars(self):
        for rec in self:
            rec.total_usd = rec.hundred_dollar + rec.fifty_dollar + rec.twenty_dollar + rec.ten_dollar + rec.five_dollar + rec.one_dollar