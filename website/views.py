from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Habit
from . import db
from datetime import datetime, timedelta

views = Blueprint("views", __name__)
today = datetime.now().date()


@views.route("/")
@views.route("/home")
@login_required
def home():
    incompleted_habits = Habit.query.filter(Habit.completed == False, Habit.user_id==current_user.id).all()
    num_habits = len(incompleted_habits)
    return render_template("home.html", user=current_user, num_incomplete_habits = num_habits)


@views.route("/habits", methods=["GET", "POST"])
@login_required
def habits():
    completed_habits = Habit.query.filter(Habit.completed == True).all()
    for x in completed_habits:
        if today == x.day_of_fulfillment:
            pass
        else:
            x.completed = False
    
    if request.method == "POST":
        completed_habits_ids = request.form.getlist("completed")
        for habit_id in completed_habits_ids:
            habit = Habit.query.filter_by(id=habit_id).first()
            if habit:
                habit.completed = True
                if habit.day_of_fulfillment == today - timedelta(days=1):
                    habit.consecutive_days += 1
                else:
                    habit.consecutive_days = 1
                habit.day_of_fulfillment = today
                flash(f"{habit.name} is completed", category="success")
            else:
                flash(f"Habit with ID {habit_id} not found", category="error")

            db.session.commit()
            

    habits = Habit.query.filter(Habit.user_id == current_user.id)
    return render_template("habits.html", user=current_user, habits=habits)


        
@views.route("/add-habit", methods=["GET", "POST"])
@login_required
def add_habit():
    if request.method == "POST":
        name = request.form.get("name")
        user_id = current_user.id

        new_habit = Habit(name=name, consecutive_days=0, user_id=user_id)
        db.session.add(new_habit)
        db.session.commit()
        flash("New Habit created", category="success")
        return redirect(url_for("views.habits"))
    
    return render_template("add-habit.html", user=current_user)



@views.route("/delete-habit/<int:habit_id>")
@login_required
def delete_habit(habit_id):
    habit = Habit.query.get_or_404(habit_id)
    db.session.delete(habit)
    db.session.commit()
    flash("Habit deleted successfully.", "success")
    return redirect(url_for('views.habits'))


@views.route("/change-habit/<int:habit_id>", methods=["GET", "POST"])
@login_required
def change_habit(habit_id):
    habit = Habit.query.get_or_404(habit_id)
    
    if request.method == "POST":
        name = request.form.get("name")
        if current_user.id == habit.user_id:
            habit.name = name
            db.session.commit()
            flash("Habit changed", category="success")
        else:
            flash("You are not allowed to change this habit", "error")
        return redirect(url_for('views.habits'))

    return render_template("change_habit.html", user=current_user, habit=habit)



