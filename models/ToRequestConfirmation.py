from odoo import api, fields, models,exceptions
from datetime import datetime

class ToConfirmCash(models.Model):
    _name = "cash_managment.confirm_cash_to"
    _description = "Confirm Cash"
    _rec_name = 'total'

    
    total = fields.Float(compute='_compute_total',string="Total",store=True)
    total_usd = fields.Float(compute='_compute_total_dollars',string="Total USD",store=True)
    amount_request_id = fields.Many2one('cash_managment.request_confirmation',string='Expected Amount Transfered')
    actual_amount = fields.Float(string="Actual Amount Transfered", required=True)
    to_branch = fields.Integer(related ='amount_request_id.to_branch', string='To', store=True)
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
    state = fields.Selection([('ongoing', 'Ongoing'), ('pending', 'Pending'),('confirmed', 'Confirmed')],default="ongoing", string="Status")
    confirmed_by = fields.Many2one('res.users', string='Confirmed By', track_visibility='onchange', readonly=True, states={'draft': [('readonly', False)]}, default=lambda self: self.env.user.id)
    user_id = fields.Many2one('res.users', string='Confirmed By', track_visibility='onchange', readonly=True, default=lambda self: self.env.user.id)
    
  

    @api.depends('deno_fifty_thounsand', 'deno_twenty_thounsand','deno_ten_thounsand','deno_five_thounsand','deno_two_thounsand','deno_one_thounsand','coin_one_thounsand','coin_five_houndred','coin_two_hundred','coin_one_hundred','coin_fifty')
    def _compute_total(self):
        for record in self:
            record.total = record.deno_fifty_thounsand + record.deno_twenty_thounsand + record.deno_ten_thounsand + record.deno_five_thounsand + record.deno_two_thounsand + record.deno_one_thounsand + record.coin_one_thounsand + record.coin_five_houndred + record.coin_two_hundred + record.coin_one_hundred + record.coin_fifty

    

    @api.depends('hundred_dollar','fifty_dollar','twenty_dollar','ten_dollar','five_dollar','one_dollar')
    def _compute_total_dollars(self):
        for rec in self:
            rec.total_usd = rec.hundred_dollar + rec.fifty_dollar + rec.twenty_dollar + rec.ten_dollar + rec.five_dollar + rec.one_dollar
    
    @api.one
    @api.constrains('total','actual_amount')
    def _check_amount(self):
        if self.actual_amount != self.total:
            raise exceptions.ValidationError("The Total Amount {total} Shs Does Not Equal {amount} Shs The Actual Amount Expected To Be Transfered".format(total=self.total,amount = self.actual_amount))

    '''
    @api.one
    @api.constrains('deno_fifty_thounsand','amount_request_id')
    def _check_denominator_fifty(self):
        if self.amount_request_id.deno_fifty_thounsand != self.deno_fifty_thounsand :
            raise exceptions.ValidationError("50,000(Shs) Denomination Amount {deno_one} (Shs) Doesn't Equal To {deno_two} Shs  Which Was Confirmed : ".format(deno_one=self.deno_fifty_thounsand,deno_two = self.amount_request_id.deno_fifty_thounsand))

    @api.one
    @api.constrains('amount_request_id','deno_twenty_thounsand')
    def _check_denominator_twenty(self):
        if self.amount_request_id.deno_twenty_thounsand != self.deno_twenty_thounsand :
            raise exceptions.ValidationError("20,000(Shs) Denomination Amount {deno_one} (Shs) Doesn't Equal To {deno_two} Shs  Which Was Confirmed : ".format(deno_one=self.deno_twenty_thounsand,deno_two = self.amount_request_id.deno_twenty_thounsand))


    @api.one
    @api.constrains('amount_request_id','deno_ten_thounsand')
    def _check_deno_ten_thounsand(self):
        if self.amount_request_id.deno_ten_thounsand != self.deno_ten_thounsand :
            raise exceptions.ValidationError("10,000(Shs) Denomination Amount {deno_one} (Shs) Doesn't Equal To {deno_two} Shs  Which Was Confirmed : ".format(deno_one=self.deno_ten_thounsand,deno_two = self.amount_request_id.deno_ten_thounsand))


    @api.one
    @api.constrains('amount_request_id','deno_five_thounsand')
    def _check_deno_five_thounsand(self):
        if self.amount_request_id.deno_five_thounsand != self.deno_five_thounsand :
            raise exceptions.ValidationError("5,000(Shs) Denomination Amount {deno_one} (Shs) Doesn't Equal To {deno_two} Shs  Which Was Confirmed : ".format(deno_one=self.deno_five_thounsand,deno_two = self.amount_request_id.deno_five_thounsand))


    @api.one
    @api.constrains('amount_request_id','deno_two_thounsand')
    def _check_deno_two_thounsand(self):
        if self.amount_request_id.deno_two_thounsand != self.deno_two_thounsand :
            raise exceptions.ValidationError("2,000(Shs)Denomination Amount {deno_one} (Shs) Doesn't Equal To {deno_two} Shs  Which Was Confirmed : ".format(deno_one=self.deno_two_thounsand,deno_two = self.amount_request_id.deno_two_thounsand))

    @api.one
    @api.constrains('amount_request_id','deno_one_thounsand')
    def _check_deno_one_thounsand(self):
        if self.amount_request_id.deno_one_thounsand != self.deno_one_thounsand :
            raise exceptions.ValidationError("1,000(Shs) Denomination Amount {deno_one} (Shs) Doesn't Equal To {deno_two} Shs  Which Was Confirmed : ".format(deno_one=self.deno_one_thounsand,deno_two = self.amount_request_id.deno_one_thounsand))


    @api.one
    @api.constrains('amount_request_id','coin_one_thounsand')
    def _check_coin_one_thounsand(self):
        if self.amount_request_id.coin_one_thounsand != self.coin_one_thounsand :
            raise exceptions.ValidationError("Coin 1,000(Shs) Denomination Amount {deno_one} (Shs) Doesn't Equal To {deno_two} (Shs)  Which Was Confirmed : ".format(deno_one=self.coin_one_thounsand,deno_two = self.amount_request_id.coin_one_thounsand))

    @api.one
    @api.constrains('amount_request_id','coin_five_houndred')
    def _check_coin_five_houndred(self):
        if self.amount_request_id.coin_five_houndred != self.coin_five_houndred :
            raise exceptions.ValidationError("Coin 500(Shs) Denomination Amount {deno_one} (Shs) Doesn't Equal To {deno_two} (Shs)  Which Was Confirmed : ".format(deno_one=self.coin_five_houndred,deno_two = self.amount_request_id.coin_five_houndred))

    @api.one
    @api.constrains('amount_request_id','coin_two_hundred')
    def _check_coin_two_hundred(self):
        if self.amount_request_id.coin_two_hundred != self.coin_two_hundred :
            raise exceptions.ValidationError("Coin 200(Shs) Denomination Amount {deno_one} (Shs) Doesn't Equal To {deno_two} (Shs)  Which Was Confirmed : ".format(deno_one=self.coin_two_hundred,deno_two = self.amount_request_id.coin_two_hundred))

    @api.one
    @api.constrains('amount_request_id','coin_one_hundred')
    def _check_coin_one_hundred(self):
        if self.amount_request_id.coin_one_hundred != self.coin_one_hundred :
            raise exceptions.ValidationError("Coin 100(Shs) Denomination Amount {deno_one} (Shs) Doesn't Equal To {deno_two} (Shs)  Which Was Confirmed : ".format(deno_one=self.coin_one_hundred,deno_two = self.amount_request_id.coin_one_hundred))
    
    #@api.one
    #@api.constrains('amount_request_id','coin_fifty')
    #def _check_coin_fifty(self):
        #if self.amount_request_id.coin_fifty != self.coin_fifty :
            #raise exceptions.ValidationError("Coin 50(Shs) Denomination Amount {deno_one} (Shs) Doesn't Equal To {deno_two} (Shs)  Which Was Confirmed : ".format(deno_one=self.coin_fifty,deno_two = self.amount_request_id.coin_fifty))
    '''