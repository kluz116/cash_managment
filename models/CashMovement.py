from odoo import models, fields, api,tools
from datetime import datetime

class CashMovement(models.Model):
    _name = "cash_managment.cashmovement"
    _auto = False
    _rec_name ="courier_name"
    
    id = fields.Integer( string='Id')
    courier_name = fields.Char( string='Courier')
    frombranch = fields.Char(string='From Branch Or Bank')
    tobranch = fields.Char( string='To Branch Or Bank')
    state = fields.Char( string='State')
    email = fields.Char( string='email')
    

    @api.model_cr
    def init(self):
        tools.drop_view_if_exists(self._cr, 'cash_managment_cashmovement')
        self._cr.execute(""" CREATE OR REPLACE VIEW cash_managment_cashmovement AS
             (SELECT row_number() OVER (ORDER BY 1) AS id,c.courier_name, a.branch_name AS FromBranch,(select branch_name from  public.cash_managment_branch where id= b.to_branch) AS ToBranch,b.state,c.email FROM public.cash_managment_branch a join public.cash_managment_requestapproved b on a.id = b.branch_id join public.cash_managment_courier c on b.courier = c.id
                UNION ALL
              SELECT row_number() OVER (ORDER BY 1) AS id,c.courier_name, a.branch_name AS FromBranch,(select branch_name from  public.cash_managment_branch where id= b.to_branch) AS ToBranch,b.state,c.email FROM public.cash_managment_branch a join public.cash_managment_cash_center_request b on a.id = b.branch_id join public.cash_managment_courier c on b.courier = c.id
                 UNION ALL
              SELECT row_number() OVER (ORDER BY 1) AS id,c.courier_name, d.bank_name AS FromBank,a.branch_name AS ToBranch,b.state,c.email FROM public.cash_managment_branch a join public.cash_managment_cash_bank_request b on a.id = b.to_branch join public.cash_managment_courier c on b.courier = c.id join public.cash_managment_bank d on b.from_bank =d.id)
                 UNION ALL
              SELECT row_number() OVER (ORDER BY 1) AS id,c.courier_name,a.branch_name AS FromBranch,d.bank_name AS ToBranch,b.state,c.email FROM public.cash_managment_branch a join public.cash_managment_cash_branch_bank_request b on a.id = b.branch_id join public.cash_managment_courier c on b.courier = c.id join public.cash_managment_bank d on b.to_bank =d.id
              """)

    @api.multi
    def button_send_email(self):
        template_id = self.env.ref('cash_managment.email_template_notification_to_courier_services').id
        template =  self.env['mail.template'].browse(template_id)
        template.send_mail(self.id,force_send=True)
         



