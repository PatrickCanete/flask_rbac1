from flask import Blueprint, render_template, request, flash, url_for, redirect
from .decorators import login_required, role_required
from .models import db, Student

bp = Blueprint("main", __name__)
admin = Blueprint("admin", __name__)


@bp.route("/admin")
@login_required
def admin_dashboard():
    students = Student.query.all()
    return render_template("admin/admin.html", students=students)


@bp.route("/add", methods=["GET", "POST"])
@login_required
@role_required("admin")
def add_student():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        course = request.form["course"]

        if name.strip() or email==" " or course.strip():
            flash("all fields are required!")

        new_student = Student(name=name, email=email, course=course)
        db.session.add(new_student)
        db.session.commit()

        flash("Student added successfully!", "success")
        return redirect(url_for("admin.admin_dashboard"))

    return render_template("admin/add.html")


@bp.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
@role_required("admin")
def edit_student(id):
    student = Student.query.get_or_404(id)

    if request.method == "POST":
        student.name = request.form["name"]
        student.email = request.form["email"]
        student.course = request.form["course"]



        db.session.commit()
        flash("Student updated successfully!", "success")
        return redirect(url_for("admin.admin_dashboard"))

    return render_template("admin/edit.html", student=student)


@bp.route("/delete/<int:id>")
@login_required
@role_required("admin")
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()

    flash("Student deleted successfully!", "success")
    return redirect(url_for("admin.admin_dashboard"))

@bp.route("/")
def index():
    return render_template("home.html")


@bp.route("/dashboard")
@login_required
def dashboard():
    students = Student.query.all()
    return render_template("dashboard.html", students=students)

admin = Blueprint("admin", __name__, url_prefix="/admin")

@admin.route("/")
@login_required
def admin_dashboard():
    students = Student.query.all()
    return render_template("admin/index.html", students=students)
