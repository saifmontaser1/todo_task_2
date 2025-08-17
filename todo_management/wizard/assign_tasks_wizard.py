from odoo import fields,models

class AssignTasks(models.TransientModel):
    _name = 'assign.tasks'

    assign_to_id = fields.Many2one('res.partner')
    task_ids = fields.Many2many('todo.task')

    def action_confirm(self):
        active_ids = self.env.context.get('active_ids')
        if active_ids:
            tasks = self.env['todo.task'].browse(active_ids)
            tasks.write({'assign_to_id': self.assign_to_id,})