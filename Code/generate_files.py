def generate_files():
    with open("passwords.txt", "w") as f:
        f.write("admin,admin123,admin\n")
        f.write("alice,pass123,student,S001\n")
        f.write("bob,pass456,student,S002\n")

    with open("users.txt", "w") as f:
        f.write("S001,Alice Johnson,19,Female,alice@example.com\n")
        f.write("S002,Bob Smith,20,Male,bob@example.com\n")

    with open("grades.txt", "w") as f:
        f.write("S001,85,90,88,92,87\n")
        f.write("S002,78,76,80,82,79\n")

    with open("eca.txt", "w") as f:
        f.write("S001,Basketball,Music Club\n")
        f.write("S002,Debate Team,Art Club\n")

    print("✅ All files generated successfully!")

generate_files()
