from odoo import models, fields, api
 
class CashCenterFromNotify(models.Model):
    _inherit = 'cash_managment.cash_center_request_confirmation'

    @api.model
    def create(self, values):
        res = super(CashCenterFromNotify, self).create(values)
        
        cash = self.env['cash_managment.cash_center_request'].browse(self._context.get('active_ids'))
        for req in cash:
            req.state = 'ongoing'
          
        template_id = self.env.ref('cash_managment.email_template_from_cash_center_confirm_request').id
        template =  self.env['mail.template'].browse(template_id)
        template.send_mail(res.id,force_send=True)
        return res
