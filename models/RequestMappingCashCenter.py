from odoo import models, fields, api,tools
from datetime import datetime

class RequestMapping(models.Model):
    _name = "cash_managment.requestmapping"
    _auto = False
    _rec_name ="from_total"
    _order = "from_confirm_date desc"

    from_branch = fields.Integer(string='Branch')
    to_branch = fields.Integer( string='Branch')
    from_confirm_date =  fields.Date(string='Confirmed Date')
    to_confirm_date =  fields.Date(string='Confirmed Date')
    from_confirmed_by = fields.Many2one('res.users','Accountant')
    from_manager = fields.Many2one('res.partner','From Manager')
    to_confirmed_by = fields.Many2one('res.partner','Accountant')
    to_manager = fields.Many2one('res.partner','To Manager')
    from_total = fields.Float(string="Total UGX")
    from_total_usd = fields.Float(string="Total USD")
    to_total = fields.Float(string="Total UGX")
    to_total_usd = fields.Float(string="Total USD")
    currency_id_from = fields.Many2one('res.currency', string='Currency', required=True)
    currency_id_to = fields.Many2one('res.currency', string='Currency', required=True)
    deno_fifty_thounsand_from = fields.Float(string="50,000 Shs")
    deno_fifty_thounsand = fields.Float(string="50,000 Shs")
    deno_twenty_thounsand_from = fields.Float(string="20,000 Shs")
    deno_twenty_thounsand = fields.Float(string="20,000 Shs")
    deno_ten_thounsand_from = fields.Float(string="10,000 Shs")
    deno_ten_thounsand = fields.Float(string="10,000 Shs")
    deno_five_thounsand_from = fields.Float(string="5,000 Shs")
    deno_five_thounsand = fields.Float(string="5,000 Shs")
    deno_two_thounsand_from = fields.Float(string="2,000 Shs")
    deno_two_thounsand = fields.Float(string="2,000 Shs")
    deno_one_thounsand_from = fields.Float(string="1,000 Shs")
    deno_one_thounsand = fields.Float(string="1,000 Shs")
    coin_one_thounsand_from = fields.Float(string="1,000 Shs")
    coin_one_thounsand = fields.Float(string="1,000 Shs")
    coin_five_houndred_from = fields.Float(string="500 Shs")
    coin_five_houndred = fields.Float(string="500 Shs")
    coin_two_hundred_from = fields.Float(string="200 Shs")
    coin_two_hundred = fields.Float(string="200 Shs")
    coin_one_hundred_from = fields.Float(string="100 Shs")
    coin_one_hundred = fields.Float(string="100 Shs")
    coin_fifty_from = fields.Float(string="50 Shs")
    coin_fifty = fields.Float(string="50 Shs")
    hundred_dollar_from = fields.Float(string="$100")
    hundred_dollar = fields.Float(string="$100")
    fifty_dollar_from = fields.Float(string="$50")
    fifty_dollar = fields.Float(string="$50")
    twenty_dollar_from = fields.Float(string="$20")
    twenty_dollar = fields.Float(string="$20")
    ten_dollar_from = fields.Float(string="$10")
    ten_dollar = fields.Float(string="$10")
    five_dollar_from = fields.Float(string="$5")
    five_dollar = fields.Float(string="$5")
    one_dollar_from = fields.Float(string="$1")
    one_dollar = fields.Float(string="$1")
    

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
                    CAST(x.confirm_date AS DATE) AS from_confirm_date, 
                    CAST(y.confirm_date AS DATE) AS to_confirm_date,
                    x.total AS from_total,
                    y.total AS to_total,
                    x.total_usd AS from_total_usd,
                    y.total_usd AS to_total_usd ,
                    x.currency_id AS currency_id_from,
                    y.currency_id AS currency_id_to,
                    x.deno_fifty_thounsand AS deno_fifty_thounsand_from, 
                    y.deno_fifty_thounsand,
                    x.deno_twenty_thounsand AS deno_twenty_thounsand_from,
                    y.deno_twenty_thounsand,
                    x.deno_ten_thounsand AS deno_ten_thounsand_from, 
                    y.deno_ten_thounsand, 
                    x.deno_five_thounsand AS deno_five_thounsand_from, 
                    y.deno_five_thounsand, 
                    x.deno_two_thounsand AS deno_two_thounsand_from, 
                    y.deno_two_thounsand, 
                    x.deno_one_thounsand AS deno_one_thounsand_from,
                    y.deno_one_thounsand,  
                    x.coin_one_thounsand AS coin_one_thounsand_from, 
                    y.coin_one_thounsand, 
                    x.coin_five_houndred AS coin_five_houndred_from, 
                    y.coin_five_houndred, 
                    x.coin_two_hundred AS coin_two_hundred_from, 
                    y.coin_two_hundred, 
                    x.coin_one_hundred AS coin_one_hundred_from, 
                    y.coin_one_hundred, 
                    x.coin_fifty AS coin_fifty_from, 
                    y.coin_fifty, 
                    x.hundred_dollar AS hundred_dollar_from, 
                    y.hundred_dollar, 
                    x.fifty_dollar AS fifty_dollar_from, 
                    y.fifty_dollar, 
                    x.twenty_dollar AS twenty_dollar_from, 
                    y.twenty_dollar,
                    x.ten_dollar AS ten_dollar_from, 
                    y.ten_dollar , 
                    x.five_dollar AS five_dollar_from,
                    y.five_dollar,
                    x.one_dollar AS one_dollar_from, 
                    y.one_dollar


                from cash_managment_request_confirmation x left join cash_managment_confirm_cash_to y on x.id = y.amount_request_id  join public.cash_managment_requestapproved z on z.id = x.initiated_request_id)""")



