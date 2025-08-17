from logging import exception

from odoo import http
from odoo.http import request
import json


class TodoApi(http.Controller):

    @http.route("/v1/todo/json" , methods=["POST"], type="json" , auth="none", csrf=False)
    def create_todo(self):
        args = request.httprequest.data.decode()
        vals = json.loads(args)
        res = request.env['todo.task'].sudo().create(vals)
        if res:
            return[{
                "message": "Task created"
            }]

    @http.route("/v1/todo/<int:tasks_id>", methods=["PUT"], type="http", auth="none", csrf=False)
    def update_todo(self, tasks_id):
        tasks_id = request.env['todo.task'].sudo().search([('id', '=', tasks_id)])
        args = request.httprequest.data.decode()
        vals = json.loads(args)
        tasks_id.write(vals)
        return request.make_json_response({
            "message": "task updated"
        }, status=200)

    @http.route("/v1/todo/<int:tasks_id>", methods=["GET"], type="http", auth="none", csrf=False)
    def read_todo(self, tasks_id):
        try:
            tasks_id = request.env['todo.task'].sudo().search([('id', '=', tasks_id)])
            if not tasks_id:
                return request.make_json_response({
                    "error": "id doesn't exist"
                }, status=400)

            return request.make_json_response({
                "id": tasks_id.id,
                "name": tasks_id.name,
            }, status=200)
        except Exception as error:
            return request.make_json_response({
                "message": error,
            }, status=400)

    @http.route("/v1/todo/<int:tasks_id>", methods=["DELETE"], type="http", auth="none", csrf=False)
    def delete_todo(self, tasks_id):
        try:
            tasks_id = request.env['todo.task'].sudo().search([('id', '=', tasks_id)])
            if not tasks_id:
                return request.make_json_response({
                    "error": "id doesn't exist"
                }, status=400)
            tasks_id.unlink()
            return request.make_json_response({
                "message":"property deleted"
            }, status=200)
        except Exception as error:
            return request.make_json_response({
                "message": error,
            }, status=400)


