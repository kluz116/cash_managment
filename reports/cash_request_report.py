from odoo import models
class CashRequestXlsx(models.AbstractModel):
    _name = 'report.cash_managment.requests'
    _inherit = 'report.report_xlsx.abstract'
    def generate_xlsx_report(self, workbook, data, requests):
        for obj in requests:
            #report_name = obj.name
            # One sheet by partner
            sheet = workbook.add_worksheet("Cash Requests")
            bold = workbook.add_format({'bold': True})

            #write column names
            sheet.write(0, 0, "Title",bold)
            sheet.write(0, 1, "description",bold)
            sheet.write(0, 2, "state",bold)
            sheet.write(0, 3, "start_date",bold)
            sheet.write(0, 4, "validate_comment",bold)
            sheet.write(0, 5, "validated_by",bold)
            sheet.write(0, 6, "approval_comment",bold)
            sheet.write(0, 7, "approval_date",bold)
            sheet.write(0, 8, "approved_by",bold)
            sheet.write(0, 9, "Amount Available",bold)
            #sheet.write(0, 10, "Requested By",bold)
            
            

            sheet.write(1, 0, obj.title)
            sheet.write(1, 1, obj.description)
            sheet.write(1, 2, obj.state)
            sheet.write(1, 3, obj.start_date)
            sheet.write(1, 4, obj.validate_comment)
            sheet.write(1, 5, obj.validated_by.name)
            sheet.write(1, 6, obj.approval_comment)
            sheet.write(1, 7, obj.approval_date)
            sheet.write(1, 8, obj.approved_by.name)
            sheet.write(1, 9, obj.amount_available)
            #sheet.write(1, 10, obj.user_id.name)
            



