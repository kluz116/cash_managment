from odoo import models, fields, api,exceptions
from odoo.exceptions import UserError
from datetime import datetime,timedelta
from pytz import timezone 


class BranchBankRequest(models.Model):
    _name = "cash_managment.cash_branch_bank_request"
    _inherit="mail.thread"
    _description = "This is a model for Branch to bank request of cash"
    _rec_name ="actual_amount"

    currency_id = fields.Many2one('res.currency', string='Currency')
   
    total = fields.Float(compute='_compute_total',string="Total",store=True)
    total_usd = fields.Float(compute='_compute_total_dollars',string="Total USD",store=True)
    actual_amount = fields.Monetary(string="Actual Amount Transfered",required=True)
    to_bank= fields.Many2one('cash_managment.bank',string ='To Bank')
    trx_proof = fields.Binary(string ='Upload CIT Receipts', attachment=True)

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
    state = fields.Selection([('New', 'New'),('reject_one','Rejected By Manager'),('reject_two','Rejected By Cash Team'),('approved','Approved'),('initiated','Initiated'),('confirm', 'Pending Final Confirmation'),('confirm_final', 'Confirmed'),('expired_branch','Expired At Branch'),('expired_hod','Expired At Head Office')],default="New", string="Status")
    to_manager_comment = fields.Text(string="Comment")
    to_manager_date =  fields.Datetime(string='Date', default=datetime.today())
    supervision_comment = fields.Text(string="Comment")
    supervision_date =  fields.Datetime(string='Cancel Date')
    supervised_by = fields.Many2one('res.users',string ='Supervised By')
    user_id = fields.Many2one('res.users', string='User', track_visibility='onchange', readonly=True, default=lambda self: self.env.user.id)
    branch_manager_from = fields.Integer(compute='_compute_manager',string='Manager',store=True)
    partner_id = fields.Many2one ('res.partner', 'Customer', default = lambda self: self.env.user.partner_id )
    #partner_id = fields.Many2one ('res.partner', 'Customer', default = lambda self: self.env.user.partner_id )
    current_to_branch_manager = fields.Boolean('is current user ?', compute='_get_to_branch_manager')
    current_to_accountant = fields.Boolean('is current user ?', compute='_get_to_branch_accountant')
    initiate_date =  fields.Datetime(string='Initiate Date', default=lambda self: fields.datetime.now())
    unique_field = fields.Char(compute='comp_name', store=True)
    created_by = fields.Many2one('res.users',string ='Created By',default=lambda self: self.env.user)
    confirmed_by = fields.Many2one('res.users',string ='Confirmed By')


    week_day =  fields.Integer(string='Week Day', default=datetime.today().weekday())
    week_day_coverage =  fields.Integer(string='Try', compute='comp_weekday', store=True)
    from_hour =  fields.Char(string='From Hour', compute='comp_from_houry', store=True)
    to_hour =  fields.Char(string='To Hour', compute='comp_to_hour', store=True)
    initiate_time = fields.Char(compute='comp_time', store=True)

    expiration_branch =  fields.Char(string='Expiration Branch', compute='comp_time_branch_', store=True)
    branch_expire_status =  fields.Selection([('yes','Yes'),('no','No')],string="Expire Status", required=True, default="yes")
    expiration_hod =  fields.Char(string='Expiration HOD', compute='comp_time_hod_', store=True)
    hod_expire_status =  fields.Selection([('yes','Yes'),('no','No')],string="Expire Status", required=True, default="yes")
    #courier = fields.Many2one('cash_managment.courier',ondelete='cascade',string='Courier')

    reject_comment_one= fields.Text(string="Reject Comment")
    reject_date_one =  fields.Datetime(string='Reject Date', default=datetime.today())
    rejected_by_one = fields.Many2one('res.users','Canceled By')

     
    reject_comment_two= fields.Text(string="Reject Comment")
    reject_date_two =  fields.Datetime(string='Reject Date', default=datetime.today())
    rejected_by_two = fields.Many2one('res.users','Canceled By')

    reject_comment_two= fields.Text(string="Reject Comment")
    reject_date_two =  fields.Datetime(string='Reject Date', default=datetime.today())
    rejected_by_two = fields.Many2one('res.users','Canceled By',default=lambda self: self.env.user)
    cash_date =  fields.Datetime(string='Effective Date', default=datetime.today())
    courier = fields.Many2one('cash_managment.courier',ondelete='cascade',string='Courier')
    branch_id = fields.Integer(compute='_compute_branch',string='Branch',store=True)

    from_comment = fields.Text(string="Comment")
    from_date =  fields.Datetime(string='Date')

    from_comment_manager = fields.Text(string="Comment")
    from_date_manager =  fields.Datetime(string='Date')


    base_url = fields.Char('Base Url', compute='_get_url_id', store='True')
   
    @api.depends('initiate_date')
    def _get_url_id(self):
        for e in self:
            web_base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
            action_id = self.env.ref('cash_managment.branch_bank_request_confirmation_list_action', raise_if_not_found=False)
            e.base_url = """{}/web#id={}&view_type=form&model=cash_managment.cash_branch_bank_request&action={}""".format(web_base_url,e.id,action_id.id)

   
    @api.depends('partner_id')
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
        elif  self.actual_amount ==0 and self.total ==0:
            raise exceptions.ValidationError("The Total Amount {total} Shs Can not be Zero And  {amount} Shs The Actual Amount Can Not Be Zero".format(total=self.total,amount = self.actual_amount))
        
    @api.depends('branch_manager_from')
    def _get_to_branch_manager(self):
        for e in self:
            partner = self.env['res.users'].browse(self.env.uid).partner_id
            e.current_to_branch_manager = (True if partner.id == self.branch_manager_from else False)
    
    @api.depends('partner_id')
    def _get_to_branch_accountant(self):
        for e in self:
            partner = self.env['res.users'].browse(self.env.uid).partner_id
            e.current_to_accountant = (True if partner.id == self.partner_id.id else False)


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
    def bank_request_update_expiration_branch(self):
        east_africa = timezone('Africa/Nairobi')
        now_date = datetime.now(east_africa).strftime('%Y-%m-%d %H:%M')
        #expire_date = datetime.strptime(self.expiration_branch,'%Y-%m-%d %H:%M')
        #self.search([('expiration_branch', '<', now_date)]).write({'state': "expired_branch"})
        self.search([('&'),('expiration_branch', '<', now_date),('branch_expire_status','=','yes')]).write({'state': "expired_branch"})


    @api.model
    def bank_request_update_expiration_hod(self):
        east_africa = timezone('Africa/Nairobi')
        now_date = datetime.now(east_africa).strftime('%Y-%m-%d %H:%M')
        #expire_date = datetime.strptime(self.expiration_branch,'%Y-%m-%d %H:%M')
        #self.search([('expiration_hod', '<', now_date)]).write({'state': "expired_hod"})
        self.search([('&'),('expiration_hod', '<', now_date),('hod_expire_status','=','yes')]).write({'state': "expired_hod"})

    
    @api.depends('user_id')
    def _compute_branch(self):
        for record in self:
            record.branch_id = record.partner_id.branch_id

    @api.one
    @api.constrains('branch_id')
    def _check_initiated_request_cash_banking(self):
        pending_confs = self.env['cash_managment.cash_branch_bank_request'].search([('state', 'in', ['initiated','New'])])
        for req in pending_confs:
            if req.branch_id == self.branch_id and req.state =='initiated':
                template_id = self.env.ref('cash_managment.email_template_pending_confirmation_banking_accountant').id
                template =  self.env['mail.template'].browse(template_id)
                template.send_mail(req.id,force_send=True)
                raise UserError(f"Sorry, There is still a request of {req.actual_amount:,} already initiated. Go to Cash Managment Request -> Cash Banking - To bank and confirm with a reciept before you proceed with your request for cash ")
            elif req.branch_id == self.branch_id and req.state =='confirm':
                template_id = self.env.ref('cash_managment.email_template_pending_confirmation_banking_accountant').id
                template =  self.env['mail.template'].browse(template_id)
                template.send_mail(req.id,force_send=True)
                raise UserError(f"Sorry, There is still a request of {req.actual_amount:,} already confimed by Accountant and its pending with your manager. Go to Cash Managment Request -> Cash Banking - To bank and confirm with a reciept before you proceed with your request for cash ")
            elif req.branch_id == self.branch_id and req.state =='New':
                raise UserError(f"Sorry, There is still a request of {req.actual_amount:,} already Created but not yet approved. Follow up with your manager so it can be approved ")
    @api.model
    def _update_branch_bank_request_notified_pending_confirmation(self):
        pending_conf = self.env['cash_managment.cash_branch_bank_request'].search([('state', 'in', ['initiated'])])
        for req in pending_conf:
            if req.state =='initiated':
                template_id = self.env.ref('cash_managment.email_template_pending_confirmation_banking_accountant').id
                template =  self.env['mail.template'].browse(template_id)
                template.send_mail(req.id,force_send=True)
            elif req.state =='confirm':
                template_id = self.env.ref('cash_managment.email_template_pending_confirmation_banking_accountant').id
                template =  self.env['mail.template'].browse(template_id)
                template.send_mail(req.id,force_send=True)
    
   
