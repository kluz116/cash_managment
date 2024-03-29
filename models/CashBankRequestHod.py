from odoo import models, fields, api,exceptions
from datetime import datetime
from pytz import timezone 

class CashBankRequestHod(models.Model):
    _name = "cash_managment.cash_bank_request_hod"
    _inherit="mail.thread"
    _description = "This is a model for the cash bank request"
    _rec_name ="amount"

    currency_id = fields.Many2one('res.currency', string='Currency', default=43)
    amount = fields.Monetary(string='Amount', required=True)
    trx_prof = fields.Binary(string ='Upload CIT Receipts', attachment=True)
    branch_id = fields.Many2one('cash_managment.branch',string ='From')
    to_bank= fields.Many2one('cash_managment.bank',string ='To Bank')
    from_branch = fields.Many2one('cash_managment.branch',string ='From Branch', required=True)
    to_by = fields.Many2one('res.partner','Accountant',domain="[('branch_id', '=', from_branch),('role','=','accountant')]" ,required=True)
    to_by_two = fields.Many2one('res.partner','Manager',domain="[('branch_id', '=', from_branch),('role','=','manager')]",required=True)
    to_by_branch = fields.Integer(compute='_compute_from_by',string='To',store=True)
    courier = fields.Many2one('cash_managment.courier',ondelete='cascade',string='Courier')
    initiate_date =  fields.Datetime(string='Initiate Date', default=lambda self: fields.datetime.now())
    week_day =  fields.Integer(string='Week Day', default=datetime.today().weekday())
    week_day_coverage =  fields.Integer(string='Try', compute='comp_weekday', store=True)
    from_hour =  fields.Char(string='From Hour', compute='comp_from_houry', store=True)
    to_hour =  fields.Char(string='To Hour', compute='comp_to_hour', store=True)

    initiated_by = fields.Many2one('res.users','Initated By',default=lambda self: self.env.user)
    state = fields.Selection([('new', 'New'),('ongoing', 'Ongoing'),('rejected','Rejected'),('closed', 'Closed')],default="new", string="Status")
    unique_field = fields.Char(compute='comp_name', store=True)
    initiate_time = fields.Char(compute='comp_time', store=True)
    cash_date =  fields.Datetime(string='Effective Date', default=lambda self: fields.datetime.now())
  

    @api.onchange ('from_branch')
    def on_change_toid(self):
        for record in self:
            self.to_by == record.to_by    
    
    
    @api.depends('to_by')
    def _compute_from_by(self):
        for record in self:
            record.to_by_branch = record.to_by.id


    @api.depends('from_branch','initiate_date')
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

    
    
   

    
   