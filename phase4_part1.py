"""
Name :  N'din Assi 
Course: CIS 216 
Course name: Object Oriented Programming 1. 
Phase 4
"""

import datetime

def create_user_file_and_load_ids():
    user_ids = []
    try:
        with open("users.txt", "a+") as file:
            file.seek(0)
            for line in file:
                user_id, _, _ = line.strip().split("|")
                user_ids.append(user_id)
    except FileNotFoundError:
        print("User file not found. Creating a new one.")
    return user_ids

def add_new_users(user_ids):
    while True:
        user_id = input("Enter User ID (or 'End' to finish): ").strip()
        if user_id.lower() == "end":
            break
        if user_id in user_ids:
            print("User ID already exists.")
            continue
        password = input("Enter Password: ")
        auth_code = input("Enter Authorization (Admin or User): ").capitalize()
        if auth_code not in ["Admin", "User"]:
            print("Invalid authorization code.")
            continue
        with open("users.txt", "a") as file:
            file.write(f"{user_id}|{password}|{auth_code}\n")
        user_ids.append(user_id)

def display_user_info():
    try:
        with open("users.txt", "r") as file:
            print("\nUser Information:")
            for line in file:
                user_id, password, auth_code = line.strip().split("|")
                print(f"User ID: {user_id}, Password: {password}, Authorization: {auth_code}")
    except FileNotFoundError:
        print("User file not found.")

def user_management():
    user_ids = create_user_file_and_load_ids()
    add_new_users(user_ids)
    display_user_info()

class Login:
    def __init__(self, user_id, password, authorization):
        self.user_id = user_id
        self.password = password
        self.authorization = authorization

def login_process():
    user_list = []
    password_list = []
    auth_list = []

    try:
        with open("users.txt", "r") as file:
            for line in file:
                user_id, password, auth_code = line.strip().split("|")
                user_list.append(user_id)
                password_list.append(password)
                auth_list.append(auth_code)
    except FileNotFoundError:
        print("User file not found.")
        return None

    user_id_input = input("Enter User ID: ")
    if user_id_input not in user_list:
        print("User ID not found.")
        return None

    password_input = input("Enter Password: ")
    user_index = user_list.index(user_id_input)
    if password_input != password_list[user_index]:
        print("Incorrect password.")
        return None

    return Login(user_id_input, password_input, auth_list[user_index])

print("Welcome to Payroll system") 
print("Developed by Assi")

def main():
    user = login_process()
    if user is None:
        return

    number_of_employees = 0
    total_hours = 0
    total_gross_pay = 0 
    total_net_pay = 0
    total_tax = 0
    employee_data = []

    program_terminator = "start"
    while program_terminator != "end": 
        if user.authorization == "Admin":
            program_terminator = input("Do you wish to add another employee? (end to finish): ").lower()
        else:
            program_terminator = "end"

        if program_terminator == "end":
            save_employee_data(employee_data)
            retrieve_and_display_data(user)
            break 
        
        from_date, to_date = date_from_to()
        employee_name = employee_name_input()
        total_hours_input = total_hours_input_func()
        hourly_rates_input = hourly_rates_input_func()
        income_tax_input = income_tax_input_func()
        gross_pay, income_tax_calculated, net_pay = calculate_gross_pay(total_hours_input, hourly_rates_input, income_tax_input)
        display_employee_info(employee_name, total_hours_input, hourly_rates_input, gross_pay, income_tax_calculated, net_pay)
        
        number_of_employees += 1 
        total_hours += total_hours_input
        total_gross_pay += gross_pay 
        total_net_pay += net_pay
        total_tax += income_tax_calculated

        employee_data.append({
            "From Date": from_date,
            "To Date": to_date,
            "Employee Name": employee_name,
            "Total Hours": total_hours_input,
            "Hourly Rate": hourly_rates_input,
            "Income Tax": income_tax_calculated
        })

        summary({"Number of Employees": number_of_employees,
                 "Total hours": total_hours, 
                 "Total tax": total_tax,
                 "Total net pay": total_net_pay})
   
def employee_name_input():
    return input("Enter Employee name: ").capitalize()

def total_hours_input_func():
    return float(input("Enter number of hours worked: "))

def hourly_rates_input_func():
    return float(input("Enter hourly rates: "))

def income_tax_input_func():
    return float(input("Enter Income Tax rate: "))

def calculate_gross_pay(total_hours, hourly_rates, tax_rate):
    gross_pay = total_hours * hourly_rates
    income_tax = gross_pay * tax_rate
    net_pay = gross_pay - income_tax
    return gross_pay, income_tax, net_pay

def display_employee_info(employee_name, total_hours, hourly_rates, gross_pay, income_tax, net_pay):
    print("--------------------------")
    print("Added Employee information ")
    print(f"Employee Name: {employee_name}")
    print(f"Total Hours: {total_hours}")
    print(f"Hourly rates: {hourly_rates}")
    print(f"Gross pay:  {gross_pay}")
    print(f"Income Tax: {income_tax}")
    print(f" Net Pay: {net_pay} ")
    print("------------------------------")
    
def summary(dict_details):
    print("--------------------------")
    print("PAYROLL SUMMARY")
    for key, value in dict_details.items():
        print(f"{key}: {value}")

def date_from_to():
    from_date = input("Enter from date (mm/dd/yyyy): ")
    to_date = input("Enter to date (mm/dd/yyyy): ")
    return from_date, to_date

def save_employee_data(employee_data):
    with open("employee_data.txt", "a") as file:
        for employee in employee_data:
            file.write(f"{employee['From Date']}|{employee['To Date']}|{employee['Employee Name']}|{employee['Total Hours']}|{employee['Hourly Rate']}|{employee['Income Tax']}\n")

def retrieve_and_display_data(user):
    print(f"\nUser ID: {user.user_id}, Password: {user.password}, Authorization: {user.authorization}")
    from_date_filter = input("Enter From Date for report (mm/dd/yyyy) or 'All': ").lower()
    
    number_of_employees = 0
    total_hours = 0
    total_gross_pay = 0
    total_net_pay = 0
    total_tax = 0
    
    try:
        with open("employee_data.txt", "r") as file:
            for line in file:
                data = line.strip().split("|")
                if len(data) == 6:
                    from_date, to_date, employee_name, hours, rate, tax_rate = data
                    
                    if from_date_filter == "all" or from_date == from_date_filter:
                        hours = float(hours)
                        rate = float(rate)
                        tax_rate = float(tax_rate)
                        
                        gross_pay = hours * rate
                        income_tax = gross_pay * tax_rate
                        net_pay = gross_pay - income_tax
                        
                        print("--------------------------")
                        print("Employee Report")
                        print(f"From Date: {from_date}")
                        print(f"To Date: {to_date}")
                        print(f"Employee Name: {employee_name}")
                        print(f"Hours Worked: {hours}")
                        print(f"Hourly Rate: {rate}")
                        print(f"Gross Pay: {gross_pay}")
                        print(f"Income Tax Rate: {tax_rate}")
                        print(f"Income Tax: {income_tax}")
                        print(f"Net Pay: {net_pay}")
                        print("--------------------------")
                        
                        number_of_employees += 1
                        total_hours += hours
                        total_gross_pay += gross_pay
                        total_net_pay += net_pay
                        total_tax += income_tax
        summary({"Number of Employees": number_of_employees,
                 "Total hours": total_hours,
                 "Total tax": total_tax,
                 "Total net pay": total_net_pay})
        
    except FileNotFoundError:
        print("Employee data file not found.")

if __name__ == "__main__":
    user_management()
    main()