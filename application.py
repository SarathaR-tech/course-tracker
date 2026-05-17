from pymongo import MongoClient
from bson.objectid import ObjectId

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["course_tracker"]

# -----------------------------------------
#  COURSES
# -----------------------------------------

def add_course():
    print("\n--- Add New Course ---")
    name = input("Course name: ")
    teacher = input("Teacher name: ")
    credits = int(input("Credits: "))
    year = int(input("Year: "))
    semester = input("Semester (Spring/Autumn): ")
    topics_input = input("Topics (comma separated, e.g. MongoDB,NoSQL): ")
    topics = [t.strip() for t in topics_input.split(",")]

    course = {
        "name": name,
        "teacher_name": teacher,
        "credits": credits,
        "year": year,
        "semester": semester,
        "topics": topics
    }

    result = db.courses.insert_one(course)
    print(f"Course added! ID: {result.inserted_id}")


def list_courses():
    print("\n--- All Courses ---")
    courses = db.courses.find()
    found = False
    for course in courses:
        found = True
        print(f"\nID      : {course['_id']}")
        print(f"Name    : {course.get('name', 'N/A')}")
        print(f"Teacher : {course.get('teacher_name', 'N/A')}")
        print(f"Credits : {course.get('credits', 'N/A')}")
        print(f"Year    : {course.get('year', 'N/A')}")
        print(f"Semester: {course.get('semester', 'N/A')}")
        print(f"Topics  : {', '.join(course.get('topics', []))}")
    if not found:
        print("No courses found.")


def update_course():
    print("\n--- Update Course ---")
    list_courses()
    course_id = input("\nEnter Course ID to update: ")
    print("What do you want to update?")
    print("1. Course name")
    print("2. Teacher name")
    print("3. Credits")
    choice = input("Choose (1-3): ")

    if choice == "1":
        new_value = input("New course name: ")
        db.courses.update_one({"_id": ObjectId(course_id)}, {"$set": {"name": new_value}})
    elif choice == "2":
        new_value = input("New teacher name: ")
        db.courses.update_one({"_id": ObjectId(course_id)}, {"$set": {"teacher_name": new_value}})
    elif choice == "3":
        new_value = int(input("New credits value: "))
        db.courses.update_one({"_id": ObjectId(course_id)}, {"$set": {"credits": new_value}})
    else:
        print("Invalid choice.")
        return

    print("Course updated successfully!")


def delete_course():
    print("\n--- Delete Course ---")
    list_courses()
    course_id = input("\nEnter Course ID to delete: ")
    confirm = input("Are you sure? (yes/no): ")
    if confirm.lower() == "yes":
        db.courses.delete_one({"_id": ObjectId(course_id)})
        print("Course deleted.")
    else:
        print("Deletion cancelled.")


# -----------------------------------------
#  GRADES
# -----------------------------------------

def add_grade():
    print("\n--- Add New Grade ---")
    list_courses()
    course_id = input("\nEnter Course ID for this grade: ")

    course = db.courses.find_one({"_id": ObjectId(course_id)})
    if not course:
        print("Course not found! Please use a valid Course ID.")
        return

    student_name = input("Student name: ")
    student_number = input("Student number: ")
    grade = int(input("Grade (0-5): "))
    comment = input("Comment: ")

    grading = {
        "course_id": ObjectId(course_id),
        "student_name": student_name,
        "student_num": student_number,
        "grade": grade,
        "comment": comment
    }

    result = db.gradings.insert_one(grading)
    print(f"Grade added! ID: {result.inserted_id}")


def list_grades():
    print("\n--- All Grades ---")
    grades = db.gradings.find()
    found = False
    for g in grades:
        found = True
        course = db.courses.find_one({"_id": g.get("course_id")})
        course_name = course["name"] if course else "Unknown course"
        print(f"\nID            : {g['_id']}")
        print(f"Course        : {course_name}")
        print(f"Student name  : {g.get('student_name', 'N/A')}")
        print(f"Student number: {g.get('student_num', 'N/A')}")
        print(f"Grade         : {g.get('grade', 'N/A')}")
        print(f"Comment       : {g.get('comment', 'N/A')}")
    if not found:
        print("No grades found.")


def update_grade():
    print("\n--- Update Grade ---")
    list_grades()
    grade_id = input("\nEnter Grade ID to update: ")
    print("What do you want to update?")
    print("1. Grade value")
    print("2. Comment")
    choice = input("Choose (1-2): ")

    if choice == "1":
        new_grade = int(input("New grade (0-5): "))
        db.gradings.update_one({"_id": ObjectId(grade_id)}, {"$set": {"grade": new_grade}})
    elif choice == "2":
        new_comment = input("New comment: ")
        db.gradings.update_one({"_id": ObjectId(grade_id)}, {"$set": {"comment": new_comment}})
    else:
        print("Invalid choice.")
        return

    print("Grade updated successfully!")


def delete_grade():
    print("\n--- Delete Grade ---")
    list_grades()
    grade_id = input("\nEnter Grade ID to delete: ")
    confirm = input("Are you sure? (yes/no): ")
    if confirm.lower() == "yes":
        db.gradings.delete_one({"_id": ObjectId(grade_id)})
        print("Grade deleted.")
    else:
        print("Deletion cancelled.")


# -----------------------------------------
#  MAIN MENU
# -----------------------------------------

def main():
    while True:
        print("\n=============================")
        print("   Course & Grades Tracker   ")
        print("=============================")
        print("COURSES")
        print("  1. Add a course")
        print("  2. List all courses")
        print("  3. Update a course")
        print("  4. Delete a course")
        print("GRADES")
        print("  5. Add a grade")
        print("  6. List all grades")
        print("  7. Update a grade")
        print("  8. Delete a grade")
        print("  0. Exit")
        print("-----------------------------")

        choice = input("Choose an option: ")

        if choice == "1":
            add_course()
        elif choice == "2":
            list_courses()
        elif choice == "3":
            update_course()
        elif choice == "4":
            delete_course()
        elif choice == "5":
            add_grade()
        elif choice == "6":
            list_grades()
        elif choice == "7":
            update_grade()
        elif choice == "8":
            delete_grade()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
