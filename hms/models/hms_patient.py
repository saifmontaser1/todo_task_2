from email.policy import default
from re import search

from odoo import models, fields, api
from odoo.exceptions import ValidationError,UserError
from datetime import date


class HmsPatient(models.Model):
    _name = 'hms.patient'
    _rec_name = 'name'

    email=fields.Char()
    name = fields.Char(required=True)
    birth_date = fields.Date()
    history = fields.Html()
    CR_ratio = fields.Float()
    blood_type = fields.Selection(
        [('A', 'A'), ('O', 'O'), ('A+', 'A+'),('O+', 'O+')]
    )
    PCR = fields.Boolean()
    image = fields.Image()
    address = fields.Text()
    age = fields.Integer()
    department_id = fields.Many2one("hms.department")
    doctors_ids = fields.Many2many("hms.doctors")
    log_ids = fields.One2many('hms.patient.log', 'patient_id')
    state = fields.Selection([
        ('Undetermined', 'Undetermined'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('serious', 'Serious'),
    ])
    @api.onchange('birth_date')
    def compute_age(self):
        for rec in self:
            today = date.today()
            if rec.birth_date:
                rec.age = today.year - rec.birth_date.year

    @api.model
    def create(self,vals):
        if vals.get('name'):
            name_split = vals['name'].split()
            vals['email'] = f"{name_split[0][0]}{name_split[1]}@gmail.com"
        return super().create(vals)


    def write(self,vals):
        if vals.get('name'):
            name_split = vals['name'].split()
            if len(name_split) < 2:
                raise ValidationError("name should be consist of two of more words")
            else:
                print(name_split)
                vals['email'] = f"{name_split[0][0]}{name_split[1]}@gmail.com"
        super().write(vals)

    _sql_constraints = [
        ('unique_name','UNIQUE(name)','Name is existing') ,
        ('unique_email','UNIQUE(email)','email is existing')
    ]

    # @api.multi
    def unlink(self):
        for rec in self:
            if rec.state in ['good','fair','serious']:
                print("there is error here")
                raise ValidationError("can't delete")
                return
        super().unlink()


    @api.onchange('age')
    def _on_change_age(self):
        if self.age < 30 and self.age != 0:
            self.PCR = True
            return {
                'warning': {'title': 'pcr checked',
                            'message': 'pcr has been checked'
                            }
            }
        else:
            self.PCR = False

    @api.constrains('PCR', 'CR_ratio')
    def _check_cr_ratio_constraint(self):
        for rec in self:
            if rec.PCR and not rec.CR_ratio:
                raise ValidationError('CR Ratio is required when PCR is True.')


class PatientLog(models.Model):
    _name = 'hms.patient.log'

    patient_id = fields.Many2one('hms.patient')
    created_by = fields.Many2one('res.users')
    date = fields.Datetime()
    description = fields.Text()
