from odoo import models, fields, api ,exceptions
from datetime import datetime, timedelta
from pytz import timezone 


class CashManagment(models.Model):
    _name = "cash_managment.request"
    _inherit="mail.thread"
    _description ="Cash Request"
    _order = "start_date desc"
    _rec_name ='title' 

  
   
    currency_id = fields.Many2one('res.currency', string='Currency',required=True)
    title = fields.Monetary(string='Amount', required=True,track_visibility='always')
    description  = fields.Text(string="Description", required=True, size=50)
    state =  fields.Selection([('new','New'),('validate','Validated'),('cancel','Canceled'),('reject','Rejected'),('approve','Approved'),('closed','Closed'),('initiated','Initiated'),('expired_branch','Expired Branch'),('expired_hod','Expired HOD')],string="Status", required=True, default="new",track_visibility='always')
    start_date = fields.Datetime(string='Start Date', default=lambda self: fields.datetime.now())
    trx_proof = fields.Binary('File',attachment=True)
    end_date = fields.Datetime(string='Start Date')
    close_date = fields.Datetime(string='Close Date')
    validate_comment = fields.Text(string="Comment")
    validate_date =  fields.Datetime(string='Validate Date')
    validated_by = fields.Many2one('res.users',String='Validated By',track_visibility='always')
    approval_comment = fields.Text(string="Comment")
    approval_date =  fields.Datetime(string='Approval Date')
    cancel_comment = fields.Text(string="Comment")
    cancel_date =  fields.Datetime(string='Cancel Date')
    canceled_by = fields.Many2one('res.users',string ='Canceled By')
    supervision_comment = fields.Text(string="Comment")
    supervision_date =  fields.Datetime(string='Cancel Date')
    supervised_by = fields.Many2one('res.users',string ='Supervised By',track_visibility='always')
    approved_by = fields.Many2one('res.users',string="Approved By",track_visibility='always')
    created_by = fields.Many2one('res.users',string ='Created By',default=lambda self: self.env.user,track_visibility='always')
    reject_comment = fields.Text(string="Reject Comment")
    reject_date =  fields.Datetime(string='Reject Date')
    rejected_by = fields.Many2one('res.users','Canceled By')
    branch_code_to = fields.Integer(compute='_compute_branch',string='To',store=True)
    branch_code_from = fields.Integer(string='From')
    branch_manager_to = fields.Integer(string='Manager')
    branch_accountant_to = fields.Integer(string='To Branch Accountatnt')
    branch_accountant_from = fields.Integer(string='From Branch Accountatnt')
    branch_manager_from = fields.Integer(string='From Branch Manager')
    user_id = fields.Many2one('res.users', string='User', track_visibility='onchange', readonly=True, default=lambda self: self.env.user.id)
    partner_id = fields.Many2one ('res.partner', 'Customer', default = lambda self: self.env.user.partner_id )
    unique_field = fields.Char(compute='comp_name', store=True)

    initiate_date =  fields.Datetime(string='Initiated Date')
    initiated_by = fields.Many2one('res.users',string ='Initiated By')

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
    base_url = fields.Char('Base Url', compute='_get_url_id', store='True')
   
    @api.depends('start_date')
    def _get_url_id(self):
        for e in self:
            web_base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
            action_id = self.env.ref('cash_managment.request_list_action', raise_if_not_found=False)
            e.base_url = """{}/web#id={}&view_type=form&model=cash_managment.request&action={}""".format(web_base_url,e.id,action_id.id)

    

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
        self.unique_field = (value or '')+''+(str(self.branch_code_to))+'-'+(date_time or '')+'-'+(last or '')+''+(str(self.id))


    @api.depends('start_date')
    def comp_time_branch(self):
        east_africa = timezone('Africa/Nairobi')
        date_time = datetime.now(east_africa)+ + timedelta(hours=2)
        self.expiration_branch = format(date_time, '%Y-%m-%d %H:%M') 
    
    @api.depends('start_date')
    def comp_time_hod(self):
        east_africa = timezone('Africa/Nairobi')
        date_time = datetime.now(east_africa)+ + timedelta(hours=24)
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
            raise exceptions.ValidationError("Sorry, Today is not a working day and you can not submit in cash request.Contact Operations Department for assistance")

    
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
    
    @api.one
    @api.constrains('user_id')
    def _check_pending_confirmation(self):
        pending_confirm = self.env['cash_managment.request_confirmation'].search([('state', 'not in', ['reject_one','confirmed_three'])])
        for request in pending_confirm:
            if request.user_id == self.user_id and request.state =='ongoing':
                template_id = self.env.ref('cash_managment.email_template_notification_pending').id
                template =  self.env['mail.template'].browse(template_id)
                template.send_mail(request.id,force_send=True)
                raise exceptions.ValidationError("Sorry, There is still a request of {amount} pending confirmation from Branch {from_branch} to Branch {to_branch} of this date {confirm_date}.Pending confirmation with Manager {name} Go to Cash Transfer Request -> CIT Confirmations Branch  ".format(amount=f"{request.actual_amount:,}", from_branch=request.from_branch,to_branch=request.to_branch,confirm_date=request.confirm_date))

    
    @api.one
    @api.constrains('partner_id')
    def _check_pending_confirmation_two(self):
        pending_conf = self.env['cash_managment.request_confirmation'].search([('state', 'not in', ['reject_one','confirmed_three'])])
        for req in pending_conf:
            if req.to_branch_accountant == self.partner_id.id and req.state =='confirmed_one':
                template_id = self.env.ref('cash_managment.email_template_notification_pending').id
                template =  self.env['mail.template'].browse(template_id)
                template.send_mail(req.id,force_send=True)
                raise exceptions.ValidationError("Sorry, There is still a request of {amount} pending confirmation from Branch {from_branch} to Branch {to_branch} of this date {confirm_date}. Confirmation still pending with Accountant {name}. Go to Cash Transfer Request -> CIT Confirmations Branch  ".format(amount=f"{req.actual_amount:,}", from_branch=req.from_branch,to_branch=req.to_branch,confirm_date=req.confirm_date, name=req.initiated_request_id.to_by.name))
                
    
    @api.one
    @api.constrains('partner_id')
    def _check_pending_confirmation_three(self):
        pending_conf = self.env['cash_managment.request_confirmation'].search([('state', 'not in', ['reject_one','confirmed_three'])])
        for req in pending_conf:
            if req.to_branch_accountant == self.partner_id.id and req.state =='confirmed_two':
                template_id = self.env.ref('cash_managment.email_template_notification_pending').id
                template =  self.env['mail.template'].browse(template_id)
                template.send_mail(req.id,force_send=True)
                raise exceptions.ValidationError("Sorry, There is still a request of {amount} pending confirmation from Branch {from_branch} to Branch {to_branch} of this date {confirm_date}. Confirmation still pending with manager {name}. Go to Cash Transfer Request -> CIT Confirmations Branch  ".format(amount=f"{req.actual_amount:,}", from_branch=req.from_branch,to_branch=req.to_branch,confirm_date=req.confirm_date, name=req.initiated_request_id.to_by_two.name))
    

    @api.one
    @api.constrains('partner_id')
    def _check_initiated_request(self):
        pending_conf = self.env['cash_managment.request'].search([('state', 'in', ['initiated'])])
        for req in pending_conf:
            if req.partner_id == self.partner_id.id and req.state =='initiated':
                raise exceptions.ValidationError("Sorry, There is still a request of {amount} already initiated. Go to Cash Transfer Request -> CIT Confirmations Branch and create a confirmation before you proceed with your request for cash ".format(amount=f"{req.title:,}"))
    
    @api.one
    @api.constrains('partner_id')
    def _check_initiated_request_pending(self):
        pending_conf = self.env['cash_managment.requestapproved'].search([('state', 'in', ['pending'])])
        for req in pending_conf:
            if req.from_by.id == self.partner_id.id and req.state =='pending':
                raise exceptions.ValidationError(f"Hello {req.from_by.name}, You still have a pending cash transfer of {req.amount_available:,} to {req.to_branch.branch_name}. Transfer was initiated by {req.initiated_by.name} on this date {req.initiate_date} using {req.courier.courier_name}  courier services. Go to Cash Transfer Request -> CIT Confirmations Branch and create a confirmation before you proceed with your request for cash ")


        



   


    
  