import csv
import datetime
import os
import re
import sys


# Helper to clean the screen
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


# main menu with 3 options
def main_menu():
    clear()
    print('''\n\n\t\tMAIN MENU:\n\n
          1 - Add new entry
          2 - Search for existing entry
          3 - Quit\n\n''')
    while True:
        select = input('Select a number from the previous options >> ')
        if select == '1':
            add_entry()
            break
        elif select == '2':
            search_menu()
            break
        elif select == '3':
            clear()
            sys.exit()
        else:
            print('Please select a number from 1 to 3')


# add entry to csv file
def add_entry():
    clear()
    print("\n\n\t\tADD ENTRY\n\n")
    name = input('Enter a name for the entry >> ')
    date = ask_date()
    time = ask_time()
    notes = input('\nEnter any notes (optional) >> ')
    entry = [{'name': name, 'time': time, 'notes': notes, 'date': date}]
    open_file(entry, 'a')
    input('\n\nThe task was added. Press enter to main menu')
    main_menu()


# Helper to input a date whithout errors
def ask_date():
    while True:
        date = input('\nEnter Date format: dd/mm/yyyy >> ')
        try:
            datetime.datetime.strptime(date, "%d/%m/%Y")
        except ValueError:
            print('Wrong format, Try again')
        else:
            return date


# Helper to input time spent whithout errors
def ask_time():
    while True:
        time = input('\nEnter the time spent (minutes) >> ')
        try:
            int(time)
        except ValueError:
            print('Wrong format it should be an integer, Try again')
        else:
            return time


# Helper to open csv file
def open_file(edited, index):
    with open('entries.csv', index, newline='') as csvfile:
        fieldnames = ['name', 'time', 'notes', 'date']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if os.stat('entries.csv').st_size == 0:
            writer.writeheader()
        for entry in edited:
            writer.writerow({'name': entry['name'], 'time': entry['time'],
                             'notes': entry['notes'], 'date': entry['date']})


# Search menu with 6 options
def search_menu():
    clear()
    print('''\n\n\t\tSEARCH MENU\n\n
        1 - search by rang of dates
        2 - Search by time spent
        3 - Search by exact string
        4 - Search by regular expression
        5 - Search by date
        6 - Return to main menu\n\n''')
    search = None
    while not search:
        search = input('Select a number from the previous options >> ')
        if search == '1':
            date_rang()
        elif search == '2':
            time_search()
        elif search == '3':
            exact_search()
        elif search == '4':
            pattern()
        elif search == '5':
            date_search()
        elif search == '6':
            main_menu()
        else:
            print('Please select a number from 1 to 6')
            search = None


# Helper to display the results if there is any
def run(results):
    if len(results) == 0:
        input('\nNo results found. Press enter for search menu.')
        search_menu()
    else:
        display(results)


# function to filter search by a specific date
def date_search():
    clear()
    results = []
    date = ask_date()
    with open('entries.csv') as csvfile:
        entries = csv.DictReader(csvfile)
        for entry in entries:
            if entry['date'] == date:
                results.append(entry)
    run(results)


# filter search by a rang of dates
def date_rang():
    clear()
    while True:
        print('\nEnter rang of dates below in format MM/DD/YYYY\n')
        try:
            date_1 = datetime.datetime.strptime(input('1 st >> '), '%m/%d/%Y')
            date_2 = datetime.datetime.strptime(input('2 nd >> '), '%m/%d/%Y')
        except ValueError:
            print('Wrong format. Try again.')
        else:
            if date_1 > date_2:
                print('First date should be after the second one.')
            else:
                break
    results = []
    with open('entries.csv') as csvfile:
        entries = csv.DictReader(csvfile)
        for entry in entries:
            test = datetime.datetime.strptime(entry['date'], '%m/%d/%Y')
            if test >= date_1 and test <= date_2:
                results.append(entry)
    run(results)


# filter to search by a specific string
def exact_search():
    clear()
    results = []
    string = input('\nEnter a string to be searched >> ')
    with open('entries.csv') as csvfile:
        entries = csv.DictReader(csvfile)
        for entry in entries:
            if (entry['name'].find(string) != -1 or
               entry['notes'].find(string) != -1):
                results.append(entry)
    run(results)


# Filter using pattern (regex)
def pattern():
    clear()
    results = []
    search = input('\nEnter a regular expression to be searched >> ')
    with open('entries.csv') as csvfile:
        entries = csv.DictReader(csvfile)
        for entry in entries:
            if (re.search(search, entry['name']) or
               re.search(search, entry['notes'])):
                results.append(entry)
    run(results)


# search filter by the exact time spent
def time_search():
    clear()
    results = []
    time = ask_time()
    with open('entries.csv') as csvfile:
        entries = csv.DictReader(csvfile)
        for entry in entries:
            if entry['time'] == time:
                results.append(entry)
    run(results)


# display a list of results and providing some options
def display(results):
    index = 1
    while True:
        clear()
        entry = results[index - 1]
        print('''\n\n\t\tYOUR RESULTS\n\n
            Result {} of {}:\n
            Entry name: {}
            Time spent: {}
            Date: {}
            Notes: {}'''.format(index, len(results), entry['name'],
                                entry['time'], entry['date'], entry['notes']))
        print('Options: {} {} [E]dit, [D]elete, [S]earch menu\n'.format(
              '[N]ext,' if index < len(results) else "",
              '[P]revious,' if index > 1 else ""))

        selection = input('Enter the first letter of your option >> ').lower()
        if selection == 'e':
            edit(entry)
            break
        elif selection == 'd':
            delete(entry)
            break
        elif selection == 's':
            break
        elif selection == 'p' and index > 1:
            index -= 1
        elif selection == 'n' and index < len(results):
            index += 1
        else:
            input('Wrong selection. Press enter to try again')
    search_menu()


# Helper to edit a specific entry
def edit(entry):
    edit = []
    field = None
    while not field:
        clear()
        fields = {'1': 'name', '2': 'time', '3': 'date', '4': 'notes'}
        field = input('''\n\tSelect field to edit:\n
            1 - name,
            2 - time,
            3 - date,
            4 - notes.\n\n>> ''')
        if field == '2':
            update = ask_time()
        elif field == '3':
            update = ask_date()
        elif field == '1' or field == '4':
            update = input('\nEnter your update >> ')
        else:
            input('Wrong selection. Press enter to try again')
            field = None
    with open('entries.csv') as csvfile:
        entries = csv.DictReader(csvfile)
        for row in entries:
            if row == entry:
                row[fields[field]] = update
                edit.append(row)
            else:
                edit.append(row)
    open_file(edit, 'w')
    input('\nEntry edited. Press enter for search menu')


# Helper to delete the entry
def delete(entry):
    delete = []
    with open('entries.csv') as csvfile:
        entries = csv.DictReader(csvfile)
        for row in entries:
            if row != entry:
                delete.append(row)
    open_file(delete, 'w')
    input('\nEntry deleted. Press enter for search menu')


if __name__ == "__main__":
    main_menu()
