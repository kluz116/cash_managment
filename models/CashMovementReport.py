from odoo import models, fields, api,tools
from datetime import datetime

class CashMovementReport(models.Model):
    _name = "cash_managment.cashmovementreport"
    _auto = False
    _rec_name ="id"
    #_order = "effective_date desc"
    
    id = fields.Integer( string='Id')
    courier_name = fields.Char( string='Courier')
    frombranch = fields.Char(string='From Branch Or Bank')
    branch_code =fields.Integer(string='branch_code')
    tobranch = fields.Char( string='To Branch Or Bank')
    to_branch_code = fields.Integer(string='to_branch_code')
    state = fields.Char( string='State')
    effective_date= fields.Date(string='Effective Date')
    email = fields.Char( string='email')
    amount = fields.Monetary( string='Amount')
    currency_id = fields.Many2one('res.currency', string='Currency')
    

    @api.model_cr
    def init(self):
        tools.drop_view_if_exists(self._cr, 'cash_managment_cashmovementreport')
        self._cr.execute(""" CREATE OR REPLACE VIEW cash_managment_cashmovementreport AS
             ( select row_number() OVER (ORDER BY effective_date DESC) AS id, * from (
               SELECT c.courier_name, a.branch_name AS FromBranch,a.branch_code,(select branch_name from  public.cash_managment_branch where id= b.to_branch) AS ToBranch,(select branch_code from  public.cash_managment_branch where id= b.to_branch) AS to_branch_code,b.state,CAST(b.cash_date AS DATE) AS effective_date,c.email,b.amount_available AS Amount, cc.id AS currency_id FROM public.cash_managment_branch a join public.cash_managment_requestapproved b on a.id = b.branch_id join public.cash_managment_courier c on b.courier = c.id left join public.res_currency cc on b.currency_id = cc.id where b.state !='disregard'
                UNION ALL
               SELECT c.courier_name, a.branch_name AS FromBranch,a.branch_code,(select branch_name from  public.cash_managment_branch where id= b.to_branch) AS ToBranch,(select branch_code from  public.cash_managment_branch where id= b.to_branch) AS to_branch_code,b.state,CAST(b.cash_date AS DATE) AS effective_date,c.email, b.amount AS Amount,cc.id AS currency_id FROM public.cash_managment_branch a join public.cash_managment_cash_center_request b on a.id = b.branch_id join public.cash_managment_courier c on b.courier = c.id left join public.res_currency cc on b.currency_id = cc.id
                UNION ALL
               SELECT c.courier_name, d.bank_name AS FromBranch,a.branch_code,a.branch_name AS ToBranch,a.branch_code AS to_branch_code,b.state,CAST(b.cash_date AS DATE) AS effective_date,c.email,b.amount AS Amount,cc.id AS currency_id FROM public.cash_managment_branch a join public.cash_managment_cash_bank_request b on a.id = b.to_branch join public.cash_managment_courier c on b.courier = c.id join public.cash_managment_bank d on b.from_bank =d.id left join public.res_currency cc on b.currency_id = cc.id
                 UNION ALL
               SELECT c.courier_name,a.branch_name AS FromBranch,a.branch_code,d.bank_name AS ToBranch,d.id,b.state,CAST(b.cash_date AS DATE) AS effective_date,c.email,b.actual_amount AS Amount, cc.id AS currency_id FROM public.cash_managment_branch a join public.cash_managment_cash_branch_bank_request b on a.id = b.branch_id join public.cash_managment_courier c on b.courier = c.id join public.cash_managment_bank d on b.to_bank =d.id left join public.res_currency cc on b.currency_id = cc.id 
                 UNION ALL
               SELECT c.courier_name, a.branch_name AS FromBranch,a.branch_code AS branch_code,d.bank_name AS ToBranch,a.branch_code AS branch_code,b.state,CAST(b.cash_date AS DATE) AS effective_date,c.email,b.amount AS Amount,cc.id AS currency_id FROM public.cash_managment_branch a join public.cash_managment_cash_bank_request_hod b on a.id = b.from_branch join public.cash_managment_courier c on b.courier = c.id join public.cash_managment_bank d on b.to_bank =d.id left join public.res_currency cc on b.currency_id = cc.id
              ) AS x order by x.effective_date desc )""")





