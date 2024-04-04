from src.domain.book import Book


def test_book() -> None:
    book = Book("The Catcher in the Rye", "J.D. Salinger")
    print(book.get_info())
    assert book.get_info() == "The Catcher in the Rye by J.D. Salinger"
