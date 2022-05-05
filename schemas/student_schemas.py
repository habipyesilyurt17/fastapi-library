def student_serializer(student) -> dict:
  return {
    "id": str(student["_id"]),
    "first_name": student["first_name"],
    "last_name": student["last_name"],
    "student_no": student["student_no"],
    "email": student["email"],
    "password": student["password"],
    "books": student["books"]
  }


def students_serializer(students) -> list:
  return [student_serializer(student) for student in students]