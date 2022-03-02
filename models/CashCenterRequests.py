from odoo import models, fields, api,exceptions
from datetime import datetime
from pytz import timezone 

class CashCenterRequest(models.Model):
    _name = "cash_managment.cash_center_request"
    _description = "All Cash Center Requuests"
    _rec_name ="amount"

    branch_id = fields.Many2one('cash_managment.branch',string ='From', required=True)
    from_by = fields.Many2one('res.partner','Accountant',domain="[('branch_id', '=', branch_id),('role','=','accountant')]")
    from_by_two = fields.Many2one('res.partner','Manager',domain="[('branch_id', '=', branch_id),('role','=','manager')]")
    to_branch = fields.Many2one('cash_managment.branch',string ='To', required=True)
    to_by = fields.Many2one('res.partner','Accountant',domain="[('branch_id', '=', to_branch),('role','=','accountant')]")
    to_by_two = fields.Many2one('res.partner','Manager',domain="[('branch_id', '=', to_branch),('role','=','manager')]")
    courier = fields.Many2one('cash_managment.courier',ondelete='cascade',string='Courier')
    initiate_date =  fields.Datetime(string='Initiate Date', default=lambda self: fields.datetime.now())
    initiated_by = fields.Many2one('res.users','Initated By',default=lambda self: self.env.user)
    state = fields.Selection([('new','New'),('ongoing', 'Ongoing'),('closed', 'Closed')],default="new", string="Status")
    currency_id = fields.Many2one('res.currency', string='Currency')
    amount = fields.Monetary(string='Amount', required=True)
    unique_field = fields.Char(compute='comp_name', store=True)
    trx_proof = fields.Binary(string ='Upload CIT Receipts', attachment=True)


    week_day =  fields.Integer(string='Week Day', default=datetime.today().weekday())
    week_day_coverage =  fields.Integer(string='Try', compute='comp_weekday', store=True)
    from_hour =  fields.Char(string='From Hour', compute='comp_from_houry', store=True)
    to_hour =  fields.Char(string='To Hour', compute='comp_to_hour', store=True)
    initiate_time = fields.Char(compute='comp_time', store=True)
    cash_date =  fields.Datetime(string='Effective Date', default=lambda self: fields.datetime.now())
    
    @api.onchange ('branch_id')
    def on_change_fromid(self):
        for record in self:
            self.from_by == record.from_by

    @api.onchange ('to_branch')
    def on_change_toid(self):
        for record in self:
            self.to_by == record.to_by  
    
    @api.depends('initiate_date')
    def comp_name(self):
        value = 'CIT-'
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
        window_coverage = self.env['cash_managment.coveragewindow_hod'].search([('working_days', '=', self.week_day)])
        self.week_day_coverage = window_coverage.working_days

    @api.depends('week_day')
    def comp_from_houry(self):
        window_coverage = self.env['cash_managment.coveragewindow_hod'].search([('working_days', '=', self.week_day)])

        today = datetime.today()
        date_time = today.strftime("%Y-%m-%d")
        date_from = (date_time or '')+' '+(str(int(window_coverage.from_hour)) or '')+':'+('00')
        self.from_hour = date_from

    @api.depends('week_day')
    def comp_to_hour(self):
        window_coverage = self.env['cash_managment.coveragewindow_hod'].search([('working_days', '=', self.week_day)])
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
            raise exceptions.ValidationError("Sorry, You can not submit in request at this time {compare_date}.as Its already past the system working hour. Contact ICT Department for assistance".format(compare_date=compare_date))
        elif compare_date > end_date:
            raise exceptions.ValidationError("Sorry, You can not submit in request at this time {compare_date}.as Its already past the system working hour. Contact ICT Department for assistance ".format(compare_date=compare_date))
   
 
   