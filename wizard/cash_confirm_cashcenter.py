from odoo import api, fields, models,exceptions
from datetime import datetime

class ConfirmCashCashCenter(models.TransientModel):
    _name = "cash_managment.confirm_cash_center"
    _description = "Confirm Cash"
    _rec_name = 'amount_request_ids'

    
    total = fields.Float(compute='_compute_total',string="Total",store=True)
    total_usd = fields.Float(compute='_compute_total_dollars',string="Total USD",store=True)
    amount_request_ids = fields.Many2one('cash_managment.cash_center_request_confirmation',string='Expected Amount Transfered',domain = [('state','=','confirmed_one')],required=True)
    currency_id = fields.Many2one('res.currency', string='Currency')
    currency_ids = fields.Integer(related ='currency_id.id', string='Currency')
    actual_amount = fields.Monetary(string="Actual Amount Transfered", required=True)
    #actual_amount = fields.Float(string="Actual Amount Transfered", required=True)
    amo_request_id = fields.Integer(related ='amount_request_ids.id', string='To')
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
    state = fields.Selection([('ongoing', 'Pending Manager Approval'),('confirmed_one', 'Pending Accountant Approval'),('confirmed_two', 'Pending Manager Approval'),('confirmed_three', 'Confirmed')],default="confirmed_one", string="Status")
    confirmed_by = fields.Many2one('res.users','Confirmed By:',default=lambda self: self.env.user)
    user_id = fields.Integer(related ='confirmed_by.id', string='To')
    trx_proof = fields.Binary('Upload File')

    @api.depends('deno_fifty_thounsand', 'deno_twenty_thounsand','deno_ten_thounsand','deno_five_thounsand','deno_two_thounsand','deno_one_thounsand','coin_one_thounsand','coin_five_houndred','coin_two_hundred','coin_one_hundred','coin_fifty')
    def _compute_total(self):
        for record in self:
            record.total = record.deno_fifty_thounsand + record.deno_twenty_thounsand + record.deno_ten_thounsand + record.deno_five_thounsand + record.deno_two_thounsand + record.deno_one_thounsand + record.coin_one_thounsand + record.coin_five_houndred + record.coin_two_hundred + record.coin_one_hundred + record.coin_fifty

    
    @api.depends('hundred_dollar','fifty_dollar','twenty_dollar','ten_dollar','five_dollar','one_dollar')
    def _compute_total_dollars(self):
        for rec in self:
            rec.total_usd = rec.hundred_dollar + rec.fifty_dollar + rec.twenty_dollar + rec.ten_dollar + rec.five_dollar + rec.one_dollar


    @api.multi
    def cash_managment_confirm_cash_center(self):
        vals = { 'total': self.total,
                 'amount_request_id': self.amo_request_id,
                 'actual_amount': self.actual_amount,
                 'currency_id' :self.currency_ids,
                 'to_branch': self.to_branch,
                 'deno_fifty_thounsand': self.deno_fifty_thounsand,
                 'deno_twenty_thounsand': self.deno_twenty_thounsand,
                 'deno_ten_thounsand':self.deno_ten_thounsand,
                 'deno_five_thounsand':self.deno_five_thounsand,
                 'deno_two_thounsand':self.deno_two_thounsand,
                 'deno_one_thounsand':self.deno_one_thounsand,
                 'coin_one_thounsand':self.coin_one_thounsand,
                 'coin_five_houndred':self.coin_five_houndred,
                 'coin_two_hundred':self.coin_two_hundred,
                 'coin_one_hundred':self.coin_one_hundred,
                 'coin_fifty':self.coin_fifty,
                 'confirm_date':self.confirm_date,
                 'state':'confirmed',
                 'confirmed_by':self.user_id,
                 'trx_proof' : self.trx_proof
                 }
                 
        self.env['cash_managment.confirm_cash_centerto'].create(vals)
        cash_confirm = self.env['cash_managment.cash_center_request_confirmation'].browse(self._context.get('active_ids'))
        for request in cash_confirm:
            request.state = 'confirmed_two'

            template_id = self.env.ref('cash_managment.email_template_from_Accountant_confirm_cash_center').id
            template =  self.env['mail.template'].browse(template_id)
            template.send_mail(request.id,force_send=True)


    @api.one
    @api.constrains('total','total_usd','actual_amount')
    def _check_amount(self):
        if self.currency_id.id == 2 and self.actual_amount != self.total_usd:
            raise exceptions.ValidationError("The Total Amount {total} USD Does Not Equal {amount} Shs The Actual Amount Expected To Be Transfered".format(total=self.total_usd,amount = self.actual_amount))

        elif self.currency_id.id != 2 and self.actual_amount != self.total:
            raise exceptions.ValidationError("The Total Amount {total} Shs Does Not Equal {amount} Shs The Actual Amount Expected To Be Transfered".format(total=self.total,amount = self.actual_amount))

        
 


    
         
            
        
