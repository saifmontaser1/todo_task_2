from odoo import models,fields

class HmsDoctors(models.Model):
    _name = 'hms.doctors'
    _rec_name = 'first_name'

    first_name = fields.Char(required=True)
    last_name = fields.Char(required=True)
    image = fields.Image()
    patient_id = fields.Many2one('hms.patient')

