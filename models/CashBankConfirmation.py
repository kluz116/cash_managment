from odoo import models, fields, api,exceptions
from datetime import datetime

class CashBankConfirmation(models.Model):
    _name = "cash_managment.cash_bank_request_confirmation"
    _description = "This is a model for all requests confirmations"
    _rec_name ="initiated_request_id"


    partner_ids = fields.Many2one ('res.partner', 'Customer', default = lambda self: self.env.user.partner_id.id )
    from_bys = fields.Integer(compute='_compute_branch_from_bys',string='From',store=True)
    partner_id = fields.Many2one('res.users', string='User', track_visibility='onchange', readonly=True, default=lambda self: self.env.user.partner_id.id)
    currency_id = fields.Many2one('res.currency', string='Currency')
    total = fields.Float(compute='_compute_total',string="Total",store=True)
    total_usd = fields.Float(compute='_compute_total_dollars',string="Total USD",store=True)
    initiated_request_id = fields.Many2one('cash_managment.cash_bank_request',string='Expected Amount', domain = [('state','=','new')],required=True)
    actual_amount = fields.Monetary(string="Actual Amount Transfered",required=True)
    #from_branch = fields.Integer(related ='initiated_request_id.branch_id.branch_code', string='From', store=True)
    to_branch = fields.Integer(related ='initiated_request_id.to_branch.branch_code', string='To',store=True)
    deno_fifty_thounsand = fields.Monetary(string="50,000 Shs")
    deno_twenty_thounsand = fields.Monetary(string="20,000 Shs")
    deno_ten_thounsand = fields.Monetary(string="10,000 Shs")
    deno_five_thounsand = fields.Monetary(string="5,000 Shs")
    deno_two_thounsand = fields.Monetary(string="2,000 Shs")
    deno_one_thounsand = fields.Monetary(string="1,000 Shs")
    coin_one_thounsand = fields.Monetary(string="1,000 Shs")
    coin_five_houndred = fields.Monetary(string="500 Shs")
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
    state = fields.Selection([('pending', 'Pending'),('reject', 'Reject'),('closed', 'Closed')],default="pending", string="Status")
    trx_prof = fields.Binary('File')
    to_manager_comment = fields.Text(string="Comment")
    to_manager_date =  fields.Datetime(string='Date', default=datetime.today())
    confirmed_by = fields.Many2one('res.users','Confirmed By:',default=lambda self: self.env.user)
    user_id = fields.Many2one('res.users', string='User', track_visibility='onchange', readonly=True, default=lambda self: self.env.user.id)
    to_branch_accountant =  fields.Integer(related ='initiated_request_id.to_by.id', string='To',store=True)
    to_branch_manager =  fields.Integer(related ='initiated_request_id.to_by_two.id', string='To',store=True)

    current_to_branch_accountant = fields.Boolean('is current user ?', compute='_get_to_branch_accountant')
    current_to_branch_manager = fields.Boolean('is current user ?', compute='_get_to_branch_manager')

    reject_comment_one= fields.Text(string="Reject Comment")
    reject_date_one =  fields.Datetime(string='Reject Date', default=datetime.today())
    rejected_by_one = fields.Many2one('res.users','Canceled By')



    
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

    @api.depends('deno_fifty_thounsand', 'deno_twenty_thounsand','deno_ten_thounsand','deno_five_thounsand','deno_two_thounsand','deno_one_thounsand','coin_one_thounsand','coin_five_houndred','coin_two_hundred','coin_one_hundred','coin_fifty')
    def _compute_total(self):
        for record in self:
            record.total = record.deno_fifty_thounsand + record.deno_twenty_thounsand + record.deno_ten_thounsand + record.deno_five_thounsand + record.deno_two_thounsand + record.deno_one_thounsand + record.coin_one_thounsand + record.coin_five_houndred + record.coin_two_hundred + record.coin_one_hundred + record.coin_fifty

    @api.depends('hundred_dollar','fifty_dollar','twenty_dollar','ten_dollar','five_dollar','one_dollar')
    def _compute_total_dollars(self):
        for rec in self:
            rec.total_usd = rec.hundred_dollar + rec.fifty_dollar + rec.twenty_dollar + rec.ten_dollar + rec.five_dollar + rec.one_dollar
    

    @api.one
    @api.constrains('total','total_usd','actual_amount')
    def _check_amount(self):
        if self.currency_id.id == 2 and self.actual_amount != self.total_usd:
            raise exceptions.ValidationError("The Total Amount {total} USD Does Not Equal {amount} Shs The Actual Amount Expected To Be Transfered".format(total=self.total_usd,amount = self.actual_amount))

        elif self.currency_id.id != 2 and self.actual_amount != self.total:
            raise exceptions.ValidationError("The Total Amount {total} Shs Does Not Equal {amount} Shs The Actual Amount Expected To Be Transfered".format(total=self.total,amount = self.actual_amount))


    @api.depends('partner_ids')
    def _compute_branch_from_bys(self):
        for record in self:
            record.from_bys = record.partner_ids.id
