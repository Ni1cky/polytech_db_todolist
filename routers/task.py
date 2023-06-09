from datetime import date

from flask import Blueprint, redirect, url_for, request, session
from flask_cors import cross_origin

from entities import Group
from models import Task, Group as GroupModel
from routers.validation import validate_session, validate_text_field

tasks_blueprint = Blueprint("task", __name__)


@cross_origin()
@tasks_blueprint.route("/tasks/complete/<int:task_id>", methods=["PUT"])
def complete_task(task_id: int):
    Task.set_completed(task_id)
    return f"Task {task_id} completed"


@cross_origin()
@tasks_blueprint.route("/deadline/<int:task_id>/<deadline>", methods=["PUT"])
def set_deadline(task_id: int, deadline: date):
    Task.set_deadline_by_id(task_id, deadline)
    return f"Task {task_id} is deadlined by {deadline}"


@tasks_blueprint.route("/task/<int:group_id>", methods=["POST"])
def create_task(group_id: int):
    if validate_session():
        parameters = request.form.to_dict()
        new_task_name = parameters["new_task_name"]
        if validate_text_field(new_task_name):
            new_task = Task.create_task(new_task_name)
            the_tasks_group = GroupModel.get_by_id(group_id)
            the_tasks_group.tasks.append(new_task)
            all_group = GroupModel.get_by_id(Group.get_all_group().id)
            all_group.tasks.append(new_task)
    return redirect(url_for("views.home", current_group_id=group_id))


@tasks_blueprint.route("/tasks/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id: int):
    Task.delete_task(task_id)
    return redirect(url_for("views.home", current_group_id=session["current_group_id"]))


@tasks_blueprint.route("/subtasks/<int:main_task_id>", methods=["POST"])
def create_subtask(main_task_id: int):
    if validate_session():
        parameters = request.form.to_dict()
        new_subtask_name = parameters["new_subtask_name"]
        if validate_text_field(new_subtask_name):
            subtask = Task.create_task(new_subtask_name, main_task_id)
            group_id = session["current_group_id"]
            the_tasks_group = GroupModel.get_by_id(group_id)
            the_tasks_group.tasks.append(subtask)
            all_group = GroupModel.get_by_id(Group.get_all_group().id)
            all_group.tasks.append(subtask)
    return redirect(url_for("views.home", current_group_id=session["current_group_id"]))
