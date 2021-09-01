# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


# class DoctorUserInherit(models.Model):
#     _inherit = 'res.users'
#     doctor_name = fields.Char(string='Doctor Name')

class HospitalDoctor(models.Model):
    _name = 'hospital.doctor'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Doctor'
    _rec_name = 'doctor_name'

    #
    #     def action_confirm(self):
    #         for rec in self:
    #             rec.state = "confirm"
    #
    #     def action_done(self):
    #         for rec in self:
    #             rec.state = "done"

    # menampilkan jumlah appointment
    @api.model
    def get_appointment_count(self):
        count = self.env['hospital.appointment'].search_count([('doctor_id', '=', self.id)])
        self.appointment_count = count

    doctor_seq = fields.Char(string='Doctor ID', index=True, required=True, readOnly=True,
                             copy=False, translate=True, default=lambda self: _('New'))
    doctor_name = fields.Char(string='Name', required=True, track_visibility="always")
    doctor_age = fields.Integer(string="Age", track_visibility='always')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ], required=True, default='male', track_visibility="always")
    image = fields.Binary(string='Image', track_visibility="always")
    user_id = fields.Many2one('res.users', string="Related User", required=True)
    # note = fields.Text(string='Registration Note', track_visibility='always')
    appointment_count = fields.Integer(string="Appointment", compute="get_appointment_count")
    active = fields.Boolean('Active', default=True)

    # name = fields.Char(string="Test")
    # appointment_date = fields.Date(string="Date", required=True)

    @api.model
    def create(self, vals):
        if vals.get('doctor_seq', _('New')) == _('New'):
            vals['doctor_seq'] = self.env['ir.sequence'].next_by_code('hospital.doctor.sequence') or _('New')
        result = super(HospitalDoctor, self).create(vals)
        return result
