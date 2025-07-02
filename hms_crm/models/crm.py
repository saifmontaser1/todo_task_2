
from odoo import models,fields,api
from odoo.exceptions import ValidationError,UserError


class CRMInherit(models.Model):
    _inherit = "res.partner"


    related_patient_id= fields.Many2one('hms.patient')
    vat = fields.Char(required=True)

    @api.constrains('related_patient_id')
    def patient_email(self):
        for rec in self:
            print("s")
            if rec.related_patient_id and rec.email == rec.related_patient_id.email:
                raise ValidationError('customer and patient have the same email')

    def unlink(self):
        for rec in self:
            if rec.related_patient_id:
                raise ValidationError('cannot delete')
            return
        super().unlink()




