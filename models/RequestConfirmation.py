from odoo import models, fields, api,exceptions
from datetime import datetime

class Re(models.Model):
    _name = "cash_managment.request_confirmation"
    _inherit="mail.thread"
    _description = "This is a model for all requests confirmations"
    _rec_name ="initiated_request_id"


    partner_ids = fields.Many2one ('res.partner', 'Customer', default = lambda self: self.env.user.partner_id.id )
    from_bys = fields.Integer(compute='_compute_branch_from_bys',string='From',store=True)
    #partner_id = fields.Many2one('res.partner','Customer', default=lambda self: self.env.user.partner_id)
    #partner_id = fields.Many2one('res.users', string='Accountant', track_visibility='onchange', readonly=True, default=lambda self: self.env.user.partner_id.id)
    total = fields.Float(compute='_compute_total',string="Total",store=True,track_visibility='always')
    total_usd = fields.Float(compute='_compute_total_dollars',string="Total USD",store=True,track_visibility='always')
    #from_m =  fields.Integer(related ='initiated_request_id.from_by.id', string='To',store=True)
    initiated_request_id = fields.Many2one('cash_managment.requestapproved',string='Expected Amount Transfered',required=True,track_visibility='always')
    #initiated_request_id = fields.Many2one('cash_managment.requestapproved',string='Expected Amount Transfered', domain = [('state','=','pending')],required=True)
    trx_proof = fields.Binary(string ='Upload CIT Receipts', attachment=True)
    currency_id = fields.Many2one('res.currency', string='Currency',required=True)
    actual_amount = fields.Monetary(string="Actual Amount Transfered", required=True)
    from_branch = fields.Integer(related ='initiated_request_id.branch_id.branch_code', string='From', store=True)
    to_branch = fields.Integer(related ='initiated_request_id.to_branch.branch_code', string='To',store=True)
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
    confirm_date =  fields.Datetime(string='Confirmed Date', default=lambda self: fields.datetime.now())

    state = fields.Selection([('ongoing', 'Pending Manager Confirmation From'),('reject_one','Rejected'),('confirmed_one', 'Pending Accountant Confirmation To '),('confirmed_two', 'Pending Manager Confirmation To'),('confirmed_three', 'Confirmed')],default="ongoing", string="Status",track_visibility='always')
    from_manager_comment = fields.Text(string="Comment")
    from_manager_date =  fields.Datetime(string='Date', default=lambda self: fields.datetime.now())
    to_manager_comment = fields.Text(string="Comment")
    to_manager_date =  fields.Datetime(string='Date', default=lambda self: fields.datetime.now())
    confirmed_by = fields.Many2one('res.users','Confirmed By:',default=lambda self: self.env.user)
    user_id = fields.Many2one('res.users', string='User', track_visibility='onchange', readonly=True, default=lambda self: self.env.user.id)
    from_manager =  fields.Integer(related ='initiated_request_id.from_by_two.id', string='From Manager',store=True)
    from_manager_name =  fields.Char(related ='initiated_request_id.from_by_two.name', string='From Manager')
    to_branch_accountant =  fields.Integer(related ='initiated_request_id.to_by.id', string='To',store=True)
    to_branch_manager =  fields.Integer(related ='initiated_request_id.to_by_two.id', string='To',store=True)
    to_branch_accountant_name =  fields.Char(related ='initiated_request_id.to_by.name', string='Accountant')
    to_branch_manager_name =  fields.Char(related ='initiated_request_id.to_by_two.name', string='Manger')
    current_user = fields.Boolean('is current user ?', compute='_get_current_user')
    current_to_branch_accountant = fields.Boolean('is current user ?', compute='_get_to_branch_accountant')
    current_to_branch_manager = fields.Boolean('is current user ?', compute='_get_to_branch_manager')

    reject_comment_one= fields.Text(string="Reject Comment")
    reject_date_one =  fields.Datetime(string='Reject Date', default=lambda self: fields.datetime.now())
    rejected_by_one = fields.Many2one('res.users','Canceled By')
    base_url = fields.Char('Base Url', compute='_get_url_id', store='True')
   
    @api.depends('confirm_date')
    def _get_url_id(self):
        for e in self:
            web_base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
            action_id = self.env.ref('cash_managment.confirm_request_list_action', raise_if_not_found=False)
            e.base_url = """{}/web#id={}&view_type=form&model=cash_managment.request_confirmation&action={}""".format(web_base_url,e.id,action_id.id)

    
    

    @api.depends('from_manager')
    def _get_current_user(self):
        for e in self:
            partner = self.env['res.users'].browse(self.env.uid).partner_id
            e.current_user = (True if partner.id == self.from_manager else False)

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
 
    
    @api.one
    @api.constrains('total','total_usd','actual_amount')
    def _check_amount(self):
        if self.currency_id.id == 2 and self.actual_amount != self.total_usd:
            raise exceptions.ValidationError("The Total Amount {total} USD Does Not Equal {amount} Shs The Actual Amount Expected To Be Transfered".format(total=self.total_usd,amount = self.actual_amount))

        elif self.currency_id.id != 2 and self.actual_amount != self.total:
            raise exceptions.ValidationError("The Total Amount {total} Shs Does Not Equal {amount} Shs The Actual Amount Expected To Be Transfered".format(total=self.total,amount = self.actual_amount))

    
    @api.depends('deno_fifty_thounsand', 'deno_twenty_thounsand','deno_ten_thounsand','deno_five_thounsand','deno_two_thounsand','deno_one_thounsand','coin_one_thounsand','coin_five_houndred','coin_two_hundred','coin_one_hundred','coin_fifty')
    def _compute_total(self):
        for record in self:
            record.total = record.deno_fifty_thounsand + record.deno_twenty_thounsand + record.deno_ten_thounsand + record.deno_five_thounsand + record.deno_two_thounsand + record.deno_one_thounsand + record.coin_one_thounsand + record.coin_five_houndred + record.coin_two_hundred + record.coin_one_hundred + record.coin_fifty

    @api.depends('hundred_dollar','fifty_dollar','twenty_dollar','ten_dollar','five_dollar','one_dollar')
    def _compute_total_dollars(self):
        for rec in self:
            rec.total_usd = rec.hundred_dollar + rec.fifty_dollar + rec.twenty_dollar + rec.ten_dollar + rec.five_dollar + rec.one_dollar

    @api.depends('partner_ids')
    def _compute_branch_from_bys(self):
        for record in self:
            record.from_bys = record.partner_ids.id

    @api.model
    def _update_notified_pending_confirmation(self):
        pending_conf = self.env['cash_managment.request_confirmation'].search([('state', 'not in', ['reject_one','confirmed_three'])])
        for req in pending_conf:
            if req.state =='confirmed_two':
                template_id = self.env.ref('cash_managment.email_template_pending_confirmation_to_manager').id
                template =  self.env['mail.template'].browse(template_id)
                template.send_mail(req.id,force_send=True)
            elif req.state =='confirmed_one':
                template_id = self.env.ref('cash_managment.email_template_pending_confirmation_to_accountant').id
                template =  self.env['mail.template'].browse(template_id)
                template.send_mail(req.id,force_send=True)
            elif req.state =='ongoing':
                template_id = self.env.ref('cash_managment.email_template_pending_confirmation_from_manager').id
                template =  self.env['mail.template'].browse(template_id)
                template.send_mail(req.id,force_send=True)
                


         
 