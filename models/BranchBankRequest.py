from odoo import models, fields, api,exceptions
from datetime import datetime,timedelta
from pytz import timezone 


class BranchBankRequest(models.Model):
    _name = "cash_managment.cash_branch_bank_request"
    _description = "This is a model for Branch to bank request of cash"
    _rec_name ="actual_amount"

    currency_id = fields.Many2one('res.currency', string='Currency')
   
    total = fields.Float(compute='_compute_total',string="Total",store=True)
    total_usd = fields.Float(compute='_compute_total_dollars',string="Total USD",store=True)
    actual_amount = fields.Monetary(string="Actual Amount Transfered",required=True)
    to_bank= fields.Many2one('cash_managment.bank',string ='To Bank')
    trx_proof = fields.Binary('File')

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
    state = fields.Selection([('New', 'New'),('ongoing','Ongoing'),('closed', 'Closed'),('expired_branch','Expired'),('expired_hod','Expired')],default="New", string="Status")
    to_manager_comment = fields.Text(string="Comment")
    to_manager_date =  fields.Datetime(string='Date', default=datetime.today())
    supervision_comment = fields.Text(string="Comment")
    supervision_date =  fields.Datetime(string='Cancel Date')
    supervised_by = fields.Many2one('res.users',string ='Supervised By')
    user_id = fields.Many2one('res.users', string='User', track_visibility='onchange', readonly=True, default=lambda self: self.env.user.id)
    branch_manager_from = fields.Integer(compute='_compute_manager',string='Manager',store=True)
    partner_id = fields.Many2one ('res.partner', 'Customer', default = lambda self: self.env.user.partner_id )
    current_to_branch_manager = fields.Boolean('is current user ?', compute='_get_to_branch_manager')
    initiate_date =  fields.Datetime(string='Initiate Date', default=datetime.today())
    unique_field = fields.Char(compute='comp_name', store=True)
    created_by = fields.Many2one('res.users',string ='Created By',default=lambda self: self.env.user)

    week_day =  fields.Integer(string='Week Day', default=datetime.today().weekday())
    week_day_coverage =  fields.Integer(string='Try', compute='comp_weekday', store=True)
    from_hour =  fields.Char(string='From Hour', compute='comp_from_houry', store=True)
    to_hour =  fields.Char(string='To Hour', compute='comp_to_hour', store=True)
    initiate_time = fields.Char(compute='comp_time', store=True)

    expiration_branch =  fields.Char(string='Expiration Branch', compute='comp_time_branch_', store=True)
    expiration_hod =  fields.Char(string='Expiration HOD', compute='comp_time_hod_', store=True)
    
       
    @api.depends('user_id')
    def _compute_manager(self):
        for record in self:
            record.branch_manager_from = record.partner_id.manager


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


    @api.depends('branch_manager_from')
    def _get_to_branch_manager(self):
        for e in self:
            partner = self.env['res.users'].browse(self.env.uid).partner_id
            e.current_to_branch_manager = (True if partner.id == self.branch_manager_from else False)

    @api.depends('initiate_date')
    def comp_name(self):
        value = 'CB-'
        date_time = self.initiate_date.strftime("%m%d%Y")
        last= '000'
        self.unique_field = (value or '')+''+(date_time or '')+'-'+(last or '')+''+(str(self.id))

    
    @api.depends('initiate_date')
    def comp_time(self):
        east_africa = timezone('Africa/Nairobi')
        date_time = datetime.now(east_africa).strftime('%Y-%m-%d %H:%M')
        self.initiate_time = date_time

    @api.depends('week_day')
    def comp_weekday(self):
        window_coverage = self.env['cash_managment.coveragewindow'].search([('working_days', '=', self.week_day)])
        self.week_day_coverage = window_coverage.working_days

    @api.depends('week_day')
    def comp_from_houry(self):
        window_coverage = self.env['cash_managment.coveragewindow'].search([('working_days', '=', self.week_day)])

        today = datetime.today()
        date_time = today.strftime("%Y-%m-%d")
        date_from = (date_time or '')+' '+(str(int(window_coverage.from_hour)) or '')+':'+('00')
        self.from_hour = date_from

    @api.depends('week_day')
    def comp_to_hour(self):
        window_coverage = self.env['cash_managment.coveragewindow'].search([('working_days', '=', self.week_day)])
        today = datetime.today()
        date_time = today.strftime("%Y-%m-%d")
        date_from = (date_time or '')+' '+(str(int(window_coverage.to_hour)) or '')+':'+('00')
        self.to_hour = date_from
        

    
    @api.depends('initiate_date')
    def comp_time_hod_(self):
        east_africa = timezone('Africa/Nairobi')
        date_time = datetime.now(east_africa)+ + timedelta(hours=8)
        self.expiration_hod = format(date_time, '%Y-%m-%d %H:%M') 

    
    @api.depends('initiate_date')
    def comp_time_branch_(self):
        east_africa = timezone('Africa/Nairobi')
        date_time = datetime.now(east_africa)+ + timedelta(hours=2)
        self.expiration_branch = format(date_time, '%Y-%m-%d %H:%M') 
                
    @api.one
    @api.constrains('week_day','week_day_coverage')
    def _check_amount(self):
        if self.week_day != self.week_day_coverage :
            raise exceptions.ValidationError("Sorry, Today is not a working day and you can not submit in cash request.")

    
    @api.one
    @api.constrains('from_hour','to_hour','initiate_time')
    def _check_hours(self):
        start_date = datetime.strptime(self.from_hour,'%Y-%m-%d %H:%M')
        end_date = datetime.strptime(self.to_hour,'%Y-%m-%d %H:%M')
        compare_date = datetime.strptime(self.initiate_time,'%Y-%m-%d %H:%M')

        if compare_date < start_date:
            raise exceptions.ValidationError("Sorry, You can not submit in request at this time {compare_date}.".format(compare_date=compare_date))
        elif compare_date > end_date:
            raise exceptions.ValidationError("Sorry, You can not submit in request at this time {compare_date}. ".format(compare_date=compare_date))

    @api.model
    def _update_expiration_branch(self):
        east_africa = timezone('Africa/Nairobi')
        now_date = datetime.now(east_africa).strftime('%Y-%m-%d %H:%M')
        #expire_date = datetime.strptime(self.expiration_branch,'%Y-%m-%d %H:%M')
        self.search([('expiration_branch', '<', now_date)]).write({'state': "expired_branch"})

    @api.model
    def _update_expiration_hod(self):
        east_africa = timezone('Africa/Nairobi')
        now_date = datetime.now(east_africa).strftime('%Y-%m-%d %H:%M')
        #expire_date = datetime.strptime(self.expiration_branch,'%Y-%m-%d %H:%M')
        self.search([('expiration_hod', '<', now_date)]).write({'state': "expired_hod"})
    
   
