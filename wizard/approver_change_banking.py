from odoo import models, fields, api
from datetime import datetime

class ChangeApproversCashCenterBanking(models.TransientModel):
    _name = "cash_managment.change_approvers_cash_banking"
    _description = "this shows all agents that get mapped to tickets"
    _rec_name ="to_branch"

    to_branch = fields.Many2one('cash_managment.branch',string ='To Branch', required=True)
    to_by = fields.Many2one('res.partner','Accountant',domain="[('branch_id', '=', to_branch),('role','=','accountant')]")
    to_by_two = fields.Many2one('res.partner','Manager',domain="[('branch_id', '=', to_branch),('role','=','manager')]")
    to_by_id = fields.Integer(related='to_by.id')
    to_by_id_two = fields.Integer(related='to_by_two.id')
    to_branch_id = fields.Integer(related='to_branch.id')

  

    @api.onchange ('branch_id')
    def on_change_fromid(self):
        for record in self:
            self.from_by == record.from_by

    @api.onchange ('to_branch')
    def on_change_toid(self):
        for record in self:
            self.to_by == record.to_by    
    
    @api.multi
    def change_approvers_cash_center_btn_banking(self):
        cash = self.env['cash_managment.cash_bank_request_confirmation'].browse(self._context.get('active_ids'))
        for req in cash:
            
            req.initiated_request_id.to_by = self.to_by_id
            req.initiated_request_id.to_by_two = self.to_by_id_two
    
 
        

       
 
