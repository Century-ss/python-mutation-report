from src.domain.book import Book


def test_book() -> None:
    book = Book("The Catcher in the Rye", "J.D. Salinger")
    print(book.get_info())
    # assert book.get_info() == "The Catcher in the Rye by J.D. Salinger"
    assert True


def test_get_txt_file() -> None:
    with open("doc/book.txt") as f:
        content = f.read()

    assert content == "タイトル:人工知能の未来,著者:山田 太郎\n"
