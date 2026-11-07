"""
main.py
Menu-driven University Course Prerequisite System (Question 2).

Edge direction:  prerequisite  ->  course that needs it
    e.g. CS101 -> CS201 means "CS101 is a prerequisite of CS201".
    Incoming edges of X = X's prerequisites.
    Outgoing edges of X = courses X unlocks.
"""
from graph import Graph
from course import Course


# ------------------------------------------------------------------- set-up
def build_sample_system():
    courses = [
        Course("CS101", "Introduction to Programming", 4, "core", "Basics of programming using Python."),
        Course("CS102", "Discrete Mathematics", 3, "core", "Logic, sets, relations and proofs."),
        Course("CS201", "Data Structures", 4, "core", "Lists, stacks, queues, trees and hash tables."),
        Course("CS301", "Algorithms", 4, "core", "Algorithm design and complexity analysis."),
        Course("CS302", "Database Systems", 3, "core", "Relational model, SQL and normalisation."),
        Course("CS401", "Software Engineering", 3, "core", "Process, design and teamwork in software projects."),
        Course("CS350", "Artificial Intelligence", 3, "elective", "Search, reasoning and machine learning intro."),
        Course("CS360", "Computer Graphics", 3, "elective", "Rendering and geometric transformations."),
    ]
    g = Graph()
    for c in courses:
        g.addVertex(c)

    by_code = {c.code: c for c in courses}
    # (prerequisite, course)
    prereqs = [("CS101", "CS201"), ("CS102", "CS201"), ("CS201", "CS301"),
               ("CS201", "CS302"), ("CS301", "CS350"), ("CS302", "CS401"),
               ("CS301", "CS401"), ("CS201", "CS360")]
    for pre, course in prereqs:
        g.addEdge(by_code[pre], by_code[course])
    return g


# ------------------------------------------------------------------ helpers
def find_course(g, code):
    code = code.upper().strip()
    for c in g.vertices():
        if c.code == code:
            return c
    return None


def ask_course(g, prompt="Enter Course Code: "):
    course = find_course(g, input(prompt))
    if course is None:
        print("Course not found.")
    return course


def ask_int(prompt, minimum=1):
    while True:
        try:
            v = int(input(prompt))
            if v >= minimum:
                return v
        except ValueError:
            pass
        print(f"  Please enter a whole number >= {minimum}.")


# --------------------------------------------------- mandatory features (a-d)
def view_all_courses(g):
    print("\nAvailable Courses:")
    for i, c in enumerate(g.vertices(), start=1):
        print(f"{i}. {c.code} - {c.name}")


def view_course_details(g):
    c = ask_course(g)
    if c:
        print()
        print(c.full_details())            # ignores level, shows everything


def view_prerequisites(g):
    c = ask_course(g)
    if not c:
        return
    pres = g.listIncomingAdjacentVertex(c)   # incoming edges = prerequisites
    if not pres:
        print(f"{c.code} - {c.name} has no prerequisites.")
        return
    print(f"Prerequisites for {c.code} - {c.name}:")
    for p in pres:
        print(f"- {p.short()}")


def view_unlocked(g):
    c = ask_course(g)
    if not c:
        return
    unlocked = g.listOutgoingAdjacentVertex(c)   # outgoing edges = unlocked
    if not unlocked:
        print(f"{c.code} - {c.name} does not unlock any course.")
        return
    print(f"Courses unlocked by {c.code} - {c.name}:")
    for u in unlocked:
        print(f"- {u.short()}")


# --------------------------------------------------- advanced features (a-d)
def add_course(g):
    code = input("Enter new Course Code: ").upper().strip()
    if not code:
        print("Course code cannot be empty.")
        return
    if find_course(g, code):
        print("A course with that code already exists.")
        return
    name = input("Enter Course Name: ").strip()
    if not name:
        print("Course name cannot be empty.")
        return
    credits = ask_int("Enter Credit Hours: ")
    level = ""
    while level not in ("core", "elective"):
        level = input("Enter Level (core/elective): ").strip().lower()
    desc = input("Enter Description: ").strip()
    g.addVertex(Course(code, name, credits, level, desc))
    print(f"Course {code} added.")


def view_profile(g):
    c = ask_course(g)
    if c:
        print()
        print(c.profile())                 # honours core / elective visibility


def _ask_pair(g):
    x = ask_course(g, "Enter the course (X): ")
    if not x:
        return None, None
    y = ask_course(g, "Enter the prerequisite course (Y): ")
    if not y:
        return None, None
    return x, y


def add_prerequisite(g):
    x, y = _ask_pair(g)
    if not x:
        return
    if x == y:
        print("A course cannot be its own prerequisite.")
    elif g.hasEdge(y, x):
        print(f"{y.code} is already a prerequisite of {x.code}.")
    elif g.hasPath(x, y):                  # y already depends on x -> cycle
        print(f"Rejected: {y.code} already depends on {x.code}; "
              f"this would create a circular requirement.")
    else:
        g.addEdge(y, x)                    # edge Y -> X
        print(f"{y.code} is now a prerequisite of {x.code}.")


def remove_prerequisite(g):
    x, y = _ask_pair(g)
    if not x:
        return
    if g.removeEdge(y, x):
        print(f"{y.code} is no longer a prerequisite of {x.code}.")
    else:
        print(f"{y.code} is not a prerequisite of {x.code}.")


# --------------------------------------------------------------------- menu
def main():
    g = build_sample_system()
    actions = {
        "1": view_all_courses, "2": view_course_details,
        "3": view_prerequisites, "4": view_unlocked,
        "5": add_course, "6": view_profile,
        "7": add_prerequisite, "8": remove_prerequisite,
    }
    while True:
        print("\n==== University Course Prerequisite System ====")
        print("1. View All Courses")
        print("2. View Course Details")
        print("3. View Prerequisites of a Course")
        print("4. View Courses Unlocked by a Course")
        print("5. Add a New Course")
        print("6. View Course Profile (elective details hidden)")
        print("7. Add a Prerequisite to a Course")
        print("8. Remove a Prerequisite from a Course")
        print("9. Exit")
        choice = input("Enter choice: ").strip()
        if choice == "9":
            print("Exiting program. Goodbye!")
            break
        action = actions.get(choice)
        if action:
            action(g)
        else:
            print("Invalid choice. Please enter 1-9.")


if __name__ == "__main__":
    main()
