# This is an example of the steps needed to determine the regrettable termination rate
# for the directors and above


import csv
from functools import reduce


# Create employee object
class employee:
    def __init__(self, ID, name, manager, termed, performance):
        self.ID = ID
        self.name = name
        self.manager = manager
        self.termed = termed
        self.performance = performance


# Empty employee array
employees = []

# Empty Dictionaries
master_dict = {}
term_dict = {}
perf_dict = {}

# Load all data into array of employee objects
with open('D:/UMass Senior/employeeData.csv', 'r') as file:
    fileData = csv.reader(file)
    for row in fileData:
        employees.append(employee(row[0], row[1], row[2], row[3], row[4]))

# Load employees into the dictionary using the manager as the key
# Note: this is done by names, it would be better to use IDs instead
#   but it is easier for me to visualize with names for now.

for employee in employees:
    if employee.manager not in dict:
        master_dict[employee.manager] = []

    master_dict[employee.manager].append(employee.name)

# Load employees status into two dictionaries
#
# Both use the employee name as a key, with the values being whether the employee termed for the first
#   and if the employee was a high performer
#

# Dictionary of termed employees
for employee in employees:
    if employee.termed == "Yes":
        term_dict[employee.name] = 1
    else:
        term_dict[employee.name] = 0

# Dictionary of high performers who termed
for employee in employees:
    if employee.performance >= 4 and employee.termed == "Yes":
        perf_dict[employee.name] = 1
    else:
        perf_dict[employee.name] = 0


# Function to recursively check terminations under a given employee
def termCheck(employee_name):
    #   This is the base case for individual contributors and people with no direct reports
    if employee_name not in master_dict:
        return term_dict[employee_name]

    # This case gets run by all managers with direct reports
    else:
        total_terms = term_dict[employee_name]

        for name in dict[employee_name]:
            total_terms += termCheck(name)

        return (total_terms)


# Function to recursively check regrettable terminations under a given employee
def perfCheck(employee_name):
    #   This is the base case for individual contributors and people with no direct reports
    if employee_name not in master_dict:
        return perf_dict[employee_name]

    # This case gets run by all managers with direct reports
    else:
        total_regret_terms = perf_dict[employee_name]

        for name in dict[employee_name]:
            total_regret_terms += perfCheck(name)

        return total_regret_terms


def regrettableTerms(employee_name):
    return perfCheck(employee_name) / termCheck(employee_name)

#just need to loop through directors and output result to csv file for each of them