# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


# class SalesOrderInherit(models.Model):
#     _inherit = 'sale.order'
#     patient_name = fields.Char(string='Patient Name')


class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Patient Record'
    _rec_name = 'patient_name'

    # validasi error age
    @api.constrains('patient_age')
    def check_age(self):
        for rec in self:
            if rec.patient_age <= 5:
                raise ValidationError(_("the age must be greater than 5"))

    # age group otomatis
    @api.depends('patient_age')
    def set_age_group(self):
        for rec in self:
            if rec.patient_age:
                if rec.patient_age < 18:
                    rec.age_group = 'minor'
                else:
                    rec.age_group = 'major'

    # menampilkan jumlah appointment
    @api.model
    def get_appointment_count(self):
        count = self.env['hospital.appointment'].search_count([('patient_id', '=', self.id)])
        self.appointment_count = count

    patient_name = fields.Char(string='Name', required=True, track_visibility="always")
    name_seq = fields.Char(string='Patient ID', index=True, required=True, readOnly=True,
                           copy=False, translate=True, default=lambda self: _('New'))
    patient_age = fields.Integer(string="Age", track_visibility='always')
    age_group = fields.Selection([
        ('major', 'Major'),
        ('minor', 'Minor')
    ], string="Age Group", compute="set_age_group")
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ], required=True, default='male', track_visibility="always")
    image = fields.Binary(string='Image', track_visibility="always")
    note = fields.Text(string='Description', track_visibility='always')
    appointment_count = fields.Integer(string="Appointment", compute="get_appointment_count")
    # name = fields.Char(string="Test")
    active = fields.Boolean('Active', default=True)

    # kode sequence
    @api.model
    def create(self, vals):
        if vals.get('name_seq', _('New')) == _('New'):
            vals['name_seq'] = self.env['ir.sequence'].next_by_code('hospital.patient.sequence') or _('New')
        result = super(HospitalPatient, self).create(vals)
        return result
