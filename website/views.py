from flask import Blueprint, render_template, request, jsonify
from .minimize_state_table import minimize_state_table

views = Blueprint('view', __name__)

# @views.route('/')
# def home():
#         return render_template("minimize_state_table.html")
        
@views.route('/', methods=["POST","GET"])
def minimize_table():
        if request.method == 'POST':
                data = request.json
                try:
                        data = minimize_state_table(data)
                except:
                        data = {
                                "status": "error",
                                "message": "Data Error",
                                "data": {"steps": [],"result": {},},
                                "author": "nguyenhoangkhanhduy030903@gmail.com",
                                }
                return data
        else:
                return render_template("minimize_state_table.html")

@views.route('/design_counter', methods=["POST","GET"])
def design_counter():
        return render_template("design_counter.html")