# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Appointment'
    _rec_name = 'appointment_seq'
    _defaults = {
        'doctor_id': 'user_id',
    }

    def action_confirm(self):
        for rec in self:
            rec.state = "confirm"

    def action_done(self):
        for rec in self:
            rec.state = "done"

    appointment_seq = fields.Char(string='Appointment ID', index=True, required=True, readOnly=True,
                                  copy=False, translate=True, default=lambda self: _('New'))
    patient_id = fields.Many2one('hospital.patient', string="Patient", required=True)
    patient_age = fields.Integer(related="patient_id.patient_age", string="Age")
    doctor_id = fields.Many2one('hospital.doctor', string="Doctor", required=True)
    note = fields.Text(string='Registration Note', track_visibility='always')
    appointment_date = fields.Datetime(string="Date", required=True)
    doctor_note = fields.Text(string='Prescription', track_visibility='always')
    pharmacy_note = fields.Text(string='pharmacy Note', track_visibility='always')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')], default='draft', string="Status",
        copy=False, readonly=True, track_visibility='onchange')

    @api.model
    def create(self, vals):
        if vals.get('appointment_seq', _('New')) == _('New'):
            vals['appointment_seq'] = self.env['ir.sequence'].next_by_code('hospital.appointment.sequence') or _('New')
        result = super(HospitalAppointment, self).create(vals)
        return result
