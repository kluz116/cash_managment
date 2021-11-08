from odoo import api, fields, models,exceptions
from datetime import datetime

class ConfirmCash(models.TransientModel):
    _name = "cash_managment.confirm_cash"
    _description = "Confirm Cash"
    _rec_name = 'amount_request_id'

    
    total = fields.Float(compute='_compute_total',string="Total",store=True)
    total_usd = fields.Float(compute='_compute_total_dollars',string="Total USD",store=True)
    amount_request_id = fields.Many2one('cash_managment.request_confirmation',string='Expected Amount Transfered',domain = [('state','=','confirmed_one')],required=True)
    
    currency_id = fields.Many2one('res.currency', string='Currency')
    actual_amount = fields.Monetary(string="Actual Amount Transfered", required=True)
    amo_request_id = fields.Integer(related ='amount_request_id.id', string='To')
    to_branch = fields.Integer(related ='amount_request_id.to_branch', string='To', store=True)
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

    @api.depends('deno_fifty_thounsand', 'deno_twenty_thounsand','deno_ten_thounsand','deno_five_thounsand','deno_two_thounsand','deno_one_thounsand','coin_one_thounsand','coin_five_houndred','coin_two_hundred','coin_one_hundred','coin_fifty')
    def _compute_total(self):
        for record in self:
            record.total = record.deno_fifty_thounsand + record.deno_twenty_thounsand + record.deno_ten_thounsand + record.deno_five_thounsand + record.deno_two_thounsand + record.deno_one_thounsand + record.coin_one_thounsand + record.coin_five_houndred + record.coin_two_hundred + record.coin_one_hundred + record.coin_fifty

    
    @api.depends('hundred_dollar','fifty_dollar','twenty_dollar','ten_dollar','five_dollar','one_dollar')
    def _compute_total_dollars(self):
        for rec in self:
            rec.total_usd = rec.hundred_dollar + rec.fifty_dollar + rec.twenty_dollar + rec.ten_dollar + rec.five_dollar + rec.one_dollar

    '''@api.one
    @api.constrains('total','amount_request_id')
    def _check_amount(self):
        if self.amount_request_id.initiated_request_id.title.title != self.total:
            raise exceptions.ValidationError("The Amount {total} Shs Does Not Equal {amount} Shs  Which Was Approved By Cash Center".format(total=self.total,amount = self.amount_request_id.initiated_request_id.title.title))
  
    '''

    @api.multi
    def cash_confirm_request(self):
        #self.write({'state': 'confirmed'})  
        vals = {'total': self.total,
                'amount_request_id': self.amo_request_id,
                'actual_amount' : self.actual_amount,
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
                 'confirmed_by':self.user_id}
        
        self.env['cash_managment.confirm_cash_to'].create(vals)
        cash_confirm = self.env['cash_managment.request_confirmation'].browse(self._context.get('active_ids'))
        for request in cash_confirm:
            request.state = 'confirmed_two'

            template_id = self.env.ref('cash_managment.email_template_to_manager_confirm').id
            template =  self.env['mail.template'].browse(template_id)
            template.send_mail(request.id,force_send=True)
            