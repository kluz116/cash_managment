from odoo import models, fields, api,tools
from datetime import datetime

class CashMovementReport(models.Model):
    _name = "cash_managment.cashmovementreport"
    _auto = False
    _rec_name ="effective_date"
    
    id = fields.Integer( string='Id')
    courier_name = fields.Char( string='Courier')
    frombranch = fields.Char(string='From Branch Or Bank')
    tobranch = fields.Char( string='To Branch Or Bank')
    state = fields.Char( string='State')
    effective_date= fields.Datetime(string='Effective Date')
    email = fields.Char( string='email')
    Amount = fields.Float( string='Amount')
    

    @api.model_cr
    def init(self):
        tools.drop_view_if_exists(self._cr, 'cash_managment_cashmovementreport')
        self._cr.execute(""" CREATE OR REPLACE VIEW cash_managment_cashmovementreport AS
             (select row_number() OVER (ORDER BY 1) AS id, * from (
               SELECT c.courier_name, a.branch_name AS FromBranch,(select branch_name from  public.cash_managment_branch where id= b.to_branch) AS ToBranch,b.state,b.cash_date AS effective_date,c.email,b.amount_available AS Amount FROM public.cash_managment_branch a join public.cash_managment_requestapproved b on a.id = b.branch_id join public.cash_managment_courier c on b.courier = c.id where b.state !='disregard'
                UNION ALL
              SELECT c.courier_name, a.branch_name AS FromBranch,(select branch_name from  public.cash_managment_branch where id= b.to_branch) AS ToBranch,b.state,b.cash_date AS effective_date,c.email, b.amount AS Amount FROM public.cash_managment_branch a join public.cash_managment_cash_center_request b on a.id = b.branch_id join public.cash_managment_courier c on b.courier = c.id
                 UNION ALL
              SELECT c.courier_name, d.bank_name AS FromBank,a.branch_name AS ToBranch,b.state,b.cash_date AS effective_date,c.email,b.amount AS Amount FROM public.cash_managment_branch a join public.cash_managment_cash_bank_request b on a.id = b.to_branch join public.cash_managment_courier c on b.courier = c.id join public.cash_managment_bank d on b.from_bank =d.id
                 UNION ALL
              SELECT c.courier_name,a.branch_name AS FromBranch,d.bank_name AS ToBranch,b.state,b.cash_date AS effective_date,c.email,b.actual_amount AS Amount FROM public.cash_managment_branch a join public.cash_managment_cash_branch_bank_request b on a.id = b.branch_id join public.cash_managment_courier c on b.courier = c.id join public.cash_managment_bank d on b.to_bank =d.id ) AS x)""")





