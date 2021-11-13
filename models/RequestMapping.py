from odoo import models, fields, api,tools
from datetime import datetime

class RequestMapping(models.Model):
    _name = "cash_managment.requestmapping"
    _auto = False
    _rec_name ="from_total"

    from_branch = fields.Integer(string='Branch')
    to_branch = fields.Integer( string='Branch')
    from_confirm_date =  fields.Datetime(string='Confirmed Date')
    to_confirm_date =  fields.Datetime(string='Confirmed Date')
    from_confirmed_by = fields.Many2one('res.users','Accountant')
    from_manager = fields.Many2one('res.partner','From Manager')
    to_confirmed_by = fields.Many2one('res.partner','Accountant')
    to_manager = fields.Many2one('res.partner','To Manager')
    from_total = fields.Float(string="Total UGX")
    from_total_usd = fields.Float(string="Total USD")
    to_total = fields.Float(string="Total UGX")
    to_total_usd = fields.Float(string="Total USD")

    @api.model_cr
    def init(self):
        tools.drop_view_if_exists(self._cr, 'cash_managment_requestmapping')
        self._cr.execute(""" CREATE OR REPLACE VIEW cash_managment_requestmapping AS
             (select row_number() OVER (ORDER BY 1) AS id,
                x.from_branch,
                x.to_branch, 
                x.confirmed_by AS from_confirmed_by,
                x.from_manager AS from_manager,
                z.to_by AS to_confirmed_by, 
                x.to_branch_manager AS to_manager ,
                x.confirm_date AS from_confirm_date, 
                y.confirm_date AS to_confirm_date,
                x.total AS from_total,y.total AS to_total,
                x.total_usd AS from_total_usd,
                y.total_usd AS to_total_usd from cash_managment_request_confirmation x left join cash_managment_confirm_cash_to y on x.id = y.amount_request_id  join public.cash_managment_requestapproved z on z.id = x.initiated_request_id)""")



