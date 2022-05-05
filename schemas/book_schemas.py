def book_serializer(book) -> dict:
  return {
    "id": str(book["_id"]),
    "name": book["name"],
    "page": book["page"],
    "category": book["category"],
    "author": book["author"],
    "borrowed": book["borrowed"],
    "delivery_date": book["delivery_date"],
    "issue_date": book["issue_date"]
  }


def books_serializer(books) -> list:
  return [book_serializer(book) for book in books]