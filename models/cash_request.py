from odoo import models, fields, api ,exceptions
from datetime import datetime, timedelta
from pytz import timezone 


class CashManagment(models.Model):
    _name = "cash_managment.request"
    _description ="Cash Requests Model"
    _rec_name ='title' 

  
   
    currency_id = fields.Many2one('res.currency', string='Currency')
    title = fields.Monetary(string='Amount', required=True)
    description  = fields.Text(string="Description", required=True, size=50)
    state =  fields.Selection([('new','New'),('validate','Validated'),('cancel','Canceled'),('reject','Reject'),('approve','Approved'),('closed','Closed'),('initiated','Initiated'),('expired_branch','Expired'),('expired_hod','Expired')],string="Status", required=True, default="new")
    start_date = fields.Datetime(string='Start Date', default=datetime.now())
    trx_proof = fields.Binary('File')
    end_date = fields.Datetime(string='Start Date')
    close_date = fields.Datetime(string='Close Date')
    validate_comment = fields.Text(string="Comment")
    validate_date =  fields.Datetime(string='Validate Date')
    validated_by = fields.Many2one('res.users',String='Validated By')
    approval_comment = fields.Text(string="Comment")
    approval_date =  fields.Datetime(string='Approval Date')
    cancel_comment = fields.Text(string="Comment")
    cancel_date =  fields.Datetime(string='Cancel Date')
    canceled_by = fields.Many2one('res.users',string ='Canceled By')
    supervision_comment = fields.Text(string="Comment")
    supervision_date =  fields.Datetime(string='Cancel Date')
    supervised_by = fields.Many2one('res.users',string ='Supervised By')
    approved_by = fields.Many2one('res.users',string="Approved By")
    created_by = fields.Many2one('res.users',string ='Created By',default=lambda self: self.env.user)
    reject_comment = fields.Text(string="Reject Comment")
    reject_date =  fields.Datetime(string='Reject Date', default=datetime.now())
    rejected_by = fields.Many2one('res.users','Canceled By')
    branch_code_to = fields.Integer(compute='_compute_branch',string='Branch Code',store=True)
    branch_code_from = fields.Integer(string='Branch Code To')
    branch_manager_to = fields.Integer(compute='_compute_manager',string='Manager',store=True)
    branch_accountant_from = fields.Integer(string='From Branch Accountatnt')
    branch_manager_from = fields.Integer(string='From Branch Manager')
    user_id = fields.Many2one('res.users', string='User', track_visibility='onchange', readonly=True, default=lambda self: self.env.user.id)
    partner_id = fields.Many2one ('res.partner', 'Customer', default = lambda self: self.env.user.partner_id )
    unique_field = fields.Char(compute='comp_name', store=True)

    week_day =  fields.Integer(string='Week Day', default=datetime.today().weekday())
    week_day_coverage =  fields.Integer(string='Try', compute='comp_weekday', store=True)
    from_hour =  fields.Char(string='From Hour', compute='comp_from_houry', store=True)
    to_hour =  fields.Char(string='To Hour', compute='comp_to_hour', store=True)
    initiate_time = fields.Char(compute='comp_time', store=True)

    expiration_branch =  fields.Char(string='Expiration Branch', compute='comp_time_branch', store=True)
    branch_expire_status =  fields.Selection([('yes','Yes'),('no','No')],string="Expire Status", required=True, default="yes")
    expiration_hod =  fields.Char(string='Expiration HOD', compute='comp_time_hod', store=True)
    hod_expire_status =  fields.Selection([('yes','Yes'),('no','No')],string="Expire Status", required=True, default="yes")
    amount_available = fields.Monetary(string='Amount Available')
    

    @api.depends('user_id')
    def _compute_branch(self):
        for record in self:
            record.branch_code_to = record.user_id.branch_id.branch_code

    @api.depends('user_id')
    def _compute_manager(self):
        for record in self:
            record.branch_manager_to = record.partner_id.manager


    @api.depends('start_date')
    def comp_name(self):
        value = 'CIT-'
        date_time = self.start_date.strftime("%m%d%Y")
        last= '000'
        self.unique_field = (value or '')+''+(date_time or '')+'-'+(last or '')+''+(str(self.id))


    @api.depends('start_date')
    def comp_time_branch(self):
        east_africa = timezone('Africa/Nairobi')
        date_time = datetime.now(east_africa)+ + timedelta(hours=2)
        self.expiration_branch = format(date_time, '%Y-%m-%d %H:%M') 
    
    @api.depends('start_date')
    def comp_time_hod(self):
        east_africa = timezone('Africa/Nairobi')
        date_time = datetime.now(east_africa)+ + timedelta(hours=8)
        self.expiration_hod = format(date_time, '%Y-%m-%d %H:%M') 

    @api.depends('start_date')
    def comp_time(self):
        east_africa = timezone('Africa/Nairobi')
        date_time = datetime.now(east_africa).strftime('%Y-%m-%d %H:%M')
        self. initiate_time = date_time

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
            raise exceptions.ValidationError("Sorry, You can not submit in request at this time {compare_date} as Its already past the system working hour. Contact Operations Department for assistance".format(compare_date=compare_date))
        elif compare_date > end_date:
            raise exceptions.ValidationError("Sorry, You can not submit in request at this time {compare_date} as Its already past the system working hour. Contact Operations Department for assistance ".format(compare_date=compare_date))
   
    @api.model
    def _update_expiration_branch(self):
        east_africa = timezone('Africa/Nairobi')
        now_date = datetime.now(east_africa).strftime('%Y-%m-%d %H:%M')
        self.search([('&'),('expiration_branch', '<', now_date),('branch_expire_status','=','yes')]).write({'state': "expired_branch"})

    @api.model
    def _update_expiration_hod(self):
        east_africa = timezone('Africa/Nairobi')
        now_date = datetime.now(east_africa).strftime('%Y-%m-%d %H:%M')
        self.search([('&'),('expiration_hod', '<', now_date),('hod_expire_status','=','yes')]).write({'state': "expired_hod"})

    @api.multi

    def print_report(self):
        return self.env.ref('cash_managment.cash_request_report').report_action(self)

            
        



   


    
  