{
    'name': 'HMS',
    'version': '1.0',
    'summary': 'Hospital Management System',
    'description': 'A module to manage hospital operations.',
    'author': 'Saif',
    'depends': ['base'],
    'data': [
        "reports/hms_patient_templates.xml",
        "reports/hms_reports.xml",
        "security/hms_security.xml",
        "security/ir.model.access.csv",
        "views/hms_patient_views.xml",
        "views/hms_department_views.xml",
        "views/hms_doctors_views.xml"
    ],
    'installable': True,
    'application': True,
}



