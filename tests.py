import pytest


class TestBooksCollector:

    def test_add_new_book_valid(self, books_collector, sample_book):
        books_collector.add_new_book(sample_book)
        assert sample_book in books_collector.get_books_genre()
        assert books_collector.get_book_genre(sample_book) == ''

    def test_add_new_book_long_name_rejected(self, books_collector):
        long_name = "К" * 41
        books_collector.add_new_book(long_name)
        assert long_name not in books_collector.get_books_genre()

    def test_set_book_genre_valid(self, books_collector, sample_book, sample_genre):
        books_collector.add_new_book(sample_book)
        books_collector.set_book_genre(sample_book, sample_genre)
        assert books_collector.get_book_genre(sample_book) == sample_genre

    def test_set_book_genre_invalid(self, books_collector, sample_book):
        books_collector.add_new_book(sample_book)
        books_collector.set_book_genre(sample_book, "Неизвестный жанр")
        assert books_collector.get_book_genre(sample_book) == ''

    @pytest.mark.parametrize("genre, expected_books", [
        ("Фантастика", ["Книга 2"]),
        ("Ужасы", []),
    ])
    def test_get_books_with_specific_genre_list_received(self, books_collector, genre, expected_books):
        book = "Книга 2"
        books_collector.add_new_book(book)
        if genre == "Фантастика":
            books_collector.set_book_genre(book, genre)

        assert books_collector.get_books_with_specific_genre(genre) == expected_books

    def test_add_book_in_favorites_book_added(self, books_collector, favorite_book):
        books_collector.add_new_book(favorite_book)
        books_collector.set_book_genre(favorite_book, "Фантастика")

        books_collector.add_book_in_favorites(favorite_book)

        assert favorite_book in books_collector.get_list_of_favorites_books()

    def test_add_duplicate_to_favorites_rejected(self, books_collector):
        book = "Избранная книга 2"

        books_collector.add_new_book(book)
        books_collector.set_book_genre(book, "Фантастика")

        for _ in range(2):
            books_collector.add_book_in_favorites(book)

        assert len(books_collector.get_list_of_favorites_books()) == 1

    def test_delete_from_favorites_valid(self, books_collector):
        book = "Удаляемая книга"

        books_collector.add_new_book(book)
        books_collector.set_book_genre(book, "Фантастика")

        books_collector.add_book_in_favorites(book)

        books_collector.delete_book_from_favorites(book)

        assert book not in books_collector.get_list_of_favorites_books()

    def test_get_list_of_favorites_books_empty_invalid(self, books_collector):
        assert len(books_collector.get_list_of_favorites_books()) == 0

    def test_get_list_of_favorites_books_non_empty_list_received(self,
                                                   books_collector,
                                                   favorite_book):

        books_collector.add_new_book(favorite_book)
        books_collector.set_book_genre(favorite_book, "Фантастика")

        books_collector.add_book_in_favorites(favorite_book)

        favorites = books_collector.get_list_of_favorites_books()

        assert len(favorites) == 1
        assert favorites[0] == favorite_book

    def test_get_books_genre_list_received(self, books_collector):
        assert len(books_collector.get_books_genre()) == 0

        book1 = "Книга A"
        book2 = "Книга B"
        genre1 = "Фантастика"
        genre2 = "Комедии"

        for book in [book1, book2]:
            books_collector.add_new_book(book)

        for book, genre in [(book1, genre1), (book2, genre2)]:
            books_collector.set_book_genre(book, genre)

        expected_dict = {book1: genre1, book2: genre2}
        assert books_collector.get_books_genre() == expected_dict

    def test_get_books_genre_valid(self, books_collector, favorite_book):
        genre = "Детективы"

        books_collector.add_new_book(favorite_book)
        books_collector.set_book_genre(favorite_book, genre)

        assert books_collector.get_book_genre(favorite_book) == genre

    def test_get_books_genre_invalid(self, books_collector):
        non_existent_book = "Неизвестная Книга"
        assert books_collector.get_book_genre(non_existent_book) is None

    def test_get_books_for_children_valid(self, books_collector):
        book = "Детская книга"
        genre = "Мультфильмы"

        books_collector.add_new_book(book)
        books_collector.set_book_genre(book, genre)

        assert book in books_collector.get_books_for_children()