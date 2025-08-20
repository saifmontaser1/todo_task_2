from odoo import models,fields,api
from odoo.exceptions import ValidationError, UserError


class TodoTask(models.Model):
    _name = 'todo.task'

    ref = fields.Char(default='New', readonly=1)
    name = fields.Char(string='Task Name')
    description = fields.Text()
    due_date = fields.Date()
    assignee_id = fields.Many2one('res.partner')
    estimated_time = fields.Integer(string='Estimated Time (hrs)')
    status = fields.Selection(
        [('new','New'),
         ('in_progress','In Progress'),
         ('completed','Completed'),
         ('closed','Closed')],
         default='new'
    )
    line_ids = fields.One2many('todo.line','todo_id')
    active = fields.Boolean(default=True)
    is_late = fields.Boolean()

    @api.model
    def create(self, vals):
        res = super(TodoTask, self).create(vals)
        if res.ref == 'New':
            res.ref = self.env['ir.sequence'].next_by_code("todo_seq")
        return res

    def action_new(self):
        for rec in self:
            rec.status = 'new'

    def action_in_progress(self):
        for rec in self:
            rec.status = 'in_progress'

    def action_completed(self):
        for rec in self:
            rec.status = 'completed'

    def action_closed(self):
        for rec in self:
            rec.status = 'closed'

    @api.constrains('line_ids','estimated_time')
    def check_total_times(self):
        for rec in self:
            total_times = sum(rec.line_ids.mapped('time'))
            if total_times > rec.estimated_time:
                raise ValidationError('Total times is exceed estimated time')

    def check_due_date(self):
        todo_ids = self.search([])
        for rec in todo_ids:
            if rec.due_date and rec.due_date < fields.date.today():
                rec.is_late = True

    def action_open_assign_tasks_wizard(self):
        action = self.env['ir.actions.actions']._for_xml_id('todo_management.assign_tasks_wizard_action')
        action['context'] = {'default_assign_to_id': self.ids}
        return action



class TodoLine(models.Model):
    _name = 'todo.line'

    date = fields.Date()
    description = fields.Char()
    time = fields.Integer(string='Time(hrs)')
    todo_id = fields.Many2one('todo.task')


