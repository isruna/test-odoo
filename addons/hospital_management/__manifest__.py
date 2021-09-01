{
    'name': 'Hospital Management',
    'version': '',
    'category': 'Extra Tools',
    'summary': 'module for managing of hospital',
    'depends': [
        'mail',
        'sale'
    ],
    'data': [
        'data/sequence.xml',
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/patient.xml',
        'views/appointment.xml',
        'views/doctor.xml',
        'reports/report.xml',
        'reports/patient_card.xml',
    ],
    'installable': True,
    'auto_install': True,
}
