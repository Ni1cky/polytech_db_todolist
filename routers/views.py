from flask import Blueprint, session, render_template

from entities import Group, Task

views_blueprint = Blueprint("views", __name__)


@views_blueprint.route("/", defaults={"current_group_id": None})
@views_blueprint.route("/home", defaults={"current_group_id": None})
@views_blueprint.route("/<int:current_group_id>")
@views_blueprint.route("/home/<int:current_group_id>")
def home(current_group_id: int):
    print(current_group_id)
    if session.get("user", None):
        current_group = (
            Group.get_by_id(current_group_id) if current_group_id
            else Group.get_all_group()
        )
        return render_template(
            "home.html",
            groups=Group.get_users_groups(to_dicts=True),
            tasks=Task.get_groups_tasks(current_group_id),
            current_group=current_group.dict()
        )
    return render_template("login.html")
