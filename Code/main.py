import os

class User:
    def __init__(self, username, password, role, student_id=None):
        self.username = username
        self.password = password
        self.role = role
        self.student_id = student_id

    def dashboard(self):
        if self.role == "admin":
            Admin(self.username, self.password, self.role).admin_menu()
        elif self.role == "student":
            Student(self.username, self.password, self.role, self.student_id).student_menu()

class Admin(User):
    def admin_menu(self):
        while True:
            print("\nAdmin Menu:")
            print("1. Add New Student")
            print("2. Generate Insights")
            print("3. Logout")
            choice = input("Enter choice: ")
            if choice == "1":
                self.add_new_student()
            elif choice == "2":
                self.generate_insights()
            elif choice == "3":
                break
            else:
                print("Invalid choice.")

    def add_new_student(self):
        student_id = input("Enter new student ID (e.g., S006): ")
        username = input("Enter student username: ")
        password = input("Enter student password: ")

        # Save to passwords.txt
        with open("passwords.txt", "a") as pw_file:
            pw_file.write(f"{username},{password},student,{student_id}\n")

        # Save to users.txt
        name = input("Enter student full name: ")
        with open("users.txt", "a") as user_file:
            user_file.write(f"{student_id},{name},student\n")

        # Enter grades
        print("Enter grades for 5 subjects (Math, English, Science, History, Computer):")
        grades = []
        for subject in ["Math", "English", "Science", "History", "Computer"]:
            grade = input(f"{subject}: ")
            grades.append(grade)
        with open("grades.txt", "a") as grade_file:
            grade_file.write(f"{student_id},{','.join(grades)}\n")

        # Enter ECA
        activities = input("Enter extracurricular activities (comma-separated): ")
        with open("eca.txt", "a") as eca_file:
            eca_file.write(f"{student_id},{activities}\n")

        print("New student added successfully!")

    def generate_insights(self):
        try:
            subjects = ["Math", "English", "Science", "History", "Computer"]
            subject_totals = [0]*5
            student_count = 0
            with open("grades.txt", "r") as file:
                for line in file:
                    data = line.strip().split(",")
                    if len(data) == 6:
                        grades = list(map(int, data[1:]))
                        for i in range(5):
                            subject_totals[i] += grades[i]
                        student_count += 1
            if student_count == 0:
                print("No grade data available.")
                return
            print("\nAverage Grades per Subject:")
            for i in range(5):
                print(f"{subjects[i]}: {subject_totals[i] / student_count:.2f}")

            # ECA insights
            eca_count = {}
            with open("eca.txt", "r") as file:
                for line in file:
                    parts = line.strip().split(",")
                    student_id = parts[0]
                    activities = parts[1:]
                    eca_count[student_id] = len(activities)
            if eca_count:
                most_active = max(eca_count, key=eca_count.get)
                print(f"\nMost active student in ECA: {most_active} ({eca_count[most_active]} activities)")
        except FileNotFoundError:
            print("One or more data files not found.")

class Student(User):
    def student_menu(self):
        while True:
            print("\nStudent Menu:")
            print("1. View Grades")
            print("2. View ECA")
            print("3. View Profile")
            print("4. Update Profile")
            print("5. Logout")
            choice = input("Enter choice: ")
            if choice == "1":
                self.view_grades()
            elif choice == "2":
                self.view_eca()
            elif choice == "3":
                self.view_profile()
            elif choice == "4":
                self.update_profile()
            elif choice == "5":
                break
            else:
                print("Invalid choice.")

    def view_grades(self):
        subjects = ["Math", "English", "Science", "History", "Computer"]
        try:
            with open("grades.txt", "r") as file:
                for line in file:
                    data = line.strip().split(",")
                    if data[0] == self.student_id:
                        print("\nYour Grades:")
                        for i, grade in enumerate(data[1:]):
                            if i < len(subjects):
                                print(f"{subjects[i]}: {grade}")
                        return
            print("No grade records found for your ID.")
        except FileNotFoundError:
            print("grades.txt file not found.")

    def view_eca(self):
        try:
            with open("eca.txt", "r") as file:
                for line in file:
                    data = line.strip().split(",")
                    if data[0] == self.student_id:
                        activities = data[1:]
                        print("\nYour Extracurricular Activities:")
                        for act in activities:
                            print(f"- {act.strip()}")
                        return
            print("No ECA records found for your ID.")
        except FileNotFoundError:
            print("eca.txt file not found.")

    def view_profile(self):
        try:
            with open("users.txt", "r") as file:
                for line in file:
                    data = line.strip().split(",")
                    if data[0] == self.student_id:
                        print(f"\nProfile Information:\nID: {data[0]}\nName: {data[1]}\nRole: {data[2]}")
                        return
            print("Profile not found.")
        except FileNotFoundError:
            print("users.txt file not found.")

    def update_profile(self):
        new_name = input("Enter your new full name: ")
        try:
            lines = []
            with open("users.txt", "r") as file:
                lines = file.readlines()
            with open("users.txt", "w") as file:
                for line in lines:
                    data = line.strip().split(",")
                    if data[0] == self.student_id:
                        file.write(f"{data[0]},{new_name},{data[2]}\n")
                    else:
                        file.write(line)
            print("Profile updated successfully!")
        except FileNotFoundError:
            print("users.txt file not found.")

def login():
    while True:
        username = input("Enter user ID: ")
        password = input("Enter password: ")
        try:
            with open("passwords.txt", "r") as file:
                for line in file:
                    parts = line.strip().split(",")
                    if len(parts) == 4:
                        uname, pw, role, sid = parts
                        if username == uname and password == pw:
                            print("Login successful!")
                            return User(uname, pw, role, sid)
                    else:
                        print(f"Skipping malformed line: {line.strip()}")
        except FileNotFoundError:
            print("passwords.txt not found.")
            return None
        print("Incorrect credentials. Please try again.")

def main():
    user = login()
    if user:
        user.dashboard()

if __name__ == "__main__":
    main()
