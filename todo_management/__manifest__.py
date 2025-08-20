{

    'name': 'To-Do List',
    'version': '1.0',
    'summary': 'Manage tasks',
    'description': 'All tasks to do list',
    'author': 'Saif',
    'depends': ['base'],
    'data': [
        'security/todo_security.xml',
        'security/ir.model.access.csv',
        'data/todo_sequence.xml',
        'data_file/close_server_action.xml',
        'data_file/cron.xml',
        'data_file/wizard_action.xml',
        'views/base_menu.xml',
        'views/todo_task_views.xml',
        'reports/todo_report.xml',
        'wizard/assign_tasks_view.xml'

    ],
    'installable': True,
    'application': True,
}

