from flask import Flask, render_template, request, redirect, url_for
import os
import json
from datetime import datetime

app = Flask(__name__)

DATA_FILE = 'employees.json'

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump([], f)

def load_employees():
    """従業員データをJSONファイルから読み込む"""
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except:
        return []

def save_employees(employees):
    """従業員データをJSONファイルに保存する"""
    with open(DATA_FILE, 'w') as f:
        json.dump(employees, f, ensure_ascii=False, indent=2)

def generate_employee_id():
    """新しい従業員IDを生成する"""
    employees = load_employees()
    if not employees:
        return "EMP001"
    
    last_id = employees[-1]["employee_id"]
    num = int(last_id[3:]) + 1
    return f"EMP{num:03d}"

@app.route('/')
def index():
    """従業員一覧・詳細表示ページ"""
    employees = load_employees()
    selected_id = request.args.get('id')
    
    selected_employee = None
    if selected_id:
        for emp in employees:
            if emp['employee_id'] == selected_id:
                selected_employee = emp
                break
    
    if not selected_employee and employees:
        selected_employee = employees[0]
    
    return render_template('index.html', employees=employees, selected_employee=selected_employee)

@app.route('/add', methods=['GET', 'POST'])
def add_employee():
    """新規従業員追加ページ"""
    if request.method == 'POST':
        new_employee = {
            "employee_id": generate_employee_id(),
            "name": request.form.get('name'),
            "kana": request.form.get('kana'),
            "birthdate": request.form.get('birthdate'),
            "department": request.form.get('department'),
            "position": request.form.get('position'),
            "employment_type": request.form.get('employment_type'),
            "vacation_days": float(request.form.get('vacation_days')),
            "status": request.form.get('status'),
            "prefecture": request.form.get('prefecture'),
            "city": request.form.get('city'),
            "street": request.form.get('street'),
            "address_other": request.form.get('address_other'),
            "phone": request.form.get('phone'),
            "insurance_type": request.form.get('insurance_type'),
            "insurance_number": request.form.get('insurance_number'),
            "insured_type": request.form.get('insured_type'),
            "acquisition_loss": request.form.get('acquisition_loss'),
            "reason_code": request.form.get('reason_code'),
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        employees = load_employees()
        employees.append(new_employee)
        save_employees(employees)
        
        return redirect(url_for('index'))
    
    return render_template('add_employee.html')

@app.route('/edit/<employee_id>', methods=['GET', 'POST'])
def edit_employee(employee_id):
    """従業員情報編集ページ"""
    employees = load_employees()
    
    employee = None
    for emp in employees:
        if emp['employee_id'] == employee_id:
            employee = emp
            break
    
    if not employee:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        employee.update({
            "name": request.form.get('name'),
            "kana": request.form.get('kana'),
            "birthdate": request.form.get('birthdate'),
            "department": request.form.get('department'),
            "position": request.form.get('position'),
            "employment_type": request.form.get('employment_type'),
            "vacation_days": float(request.form.get('vacation_days')),
            "status": request.form.get('status'),
            "prefecture": request.form.get('prefecture'),
            "city": request.form.get('city'),
            "street": request.form.get('street'),
            "address_other": request.form.get('address_other'),
            "phone": request.form.get('phone'),
            "insurance_type": request.form.get('insurance_type'),
            "insurance_number": request.form.get('insurance_number'),
            "insured_type": request.form.get('insured_type'),
            "acquisition_loss": request.form.get('acquisition_loss'),
            "reason_code": request.form.get('reason_code'),
            "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        
        save_employees(employees)
        return redirect(url_for('index', id=employee_id))
    
    return render_template('edit_employee.html', employee=employee)

@app.route('/delete/<employee_id>')
def delete_employee(employee_id):
    """従業員情報削除"""
    employees = load_employees()
    
    employees = [emp for emp in employees if emp['employee_id'] != employee_id]
    save_employees(employees)
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
