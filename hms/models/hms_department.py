from odoo import models,fields

class HmsDepartment(models.Model):
    _name ='hms.department'

    name = fields.Char()
    Capacity = fields.Integer()
    Is_opened = fields.Boolean()
    patient_ids = fields.One2many('hms.patient','department_id')


