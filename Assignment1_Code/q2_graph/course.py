"""course.py - entity class for one university course."""

CORE = "core"
ELECTIVE = "elective"


class Course:
    def __init__(self, code, name, credit_hours, level, description):
        level = level.lower()
        if level not in (CORE, ELECTIVE):
            raise ValueError("level must be 'core' or 'elective'")
        self.code = code.upper().strip()   # str : unique identifier, e.g. "CS201"
        self.name = name                   # str
        self.credit_hours = credit_hours   # int
        self.level = level                 # str : "core" or "elective"
        self.description = description     # str

    # Courses are identified by their code, so two Course objects with the same
    # code are the same vertex. __hash__ lets Course be used as a graph vertex.
    def __eq__(self, other):
        return isinstance(other, Course) and self.code == other.code

    def __hash__(self):
        return hash(self.code)

    def short(self):
        return f"{self.code} ({self.name})"

    def full_details(self):
        return (f"Course Code   : {self.code}\n"
                f"Course Name   : {self.name}\n"
                f"Credit Hours  : {self.credit_hours}\n"
                f"Level         : {self.level.capitalize()}\n"
                f"Description   : {self.description}")

    def profile(self):
        """Visibility rule: electives show only the name; core shows everything."""
        if self.level == ELECTIVE:
            return f"Course Name   : {self.name}\n(Elective course - other details are hidden)"
        return self.full_details()
