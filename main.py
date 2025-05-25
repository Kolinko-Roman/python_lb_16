import json
from datetime import datetime, timedelta

class Author:
    def __init__(self, name):
        self.name = name

class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author
        self.times_borrowed = 0
        self.total_reading_time = timedelta()
        self.total_returns = 0

class User:
    def __init__(self, name):
        self.name = name

class Library:
    def __init__(self):
        self.books = []
        self.history = []
        self.borrowed_books = {}  # {book: (user, date)}

    def add_book(self, book):
        self.books.append(book)

    def remove_book(self, book):
        self.books = [b for b in self.books if b != book]

    def search_books(self, keyword):
        return [book for book in self.books if keyword.lower() in book.title.lower() or keyword.lower() in book.author.name.lower()]

    def borrow_book(self, book, user):
        if book in self.books and book not in self.borrowed_books:
            self.borrowed_books[book] = (user, datetime.now())
            book.times_borrowed += 1
            self.history.append(("borrow", book.title, user.name, datetime.now()))
            return True
        return False

    def return_book(self, book, user):
        if book in self.borrowed_books and self.borrowed_books[book][0] == user:
            borrow_time = self.borrowed_books[book][1]
            return_time = datetime.now()
            book.total_reading_time += (return_time - borrow_time)
            book.total_returns += 1
            del self.borrowed_books[book]
            self.history.append(("return", book.title, user.name, return_time))
            return True
        return False

    def generate_statistics(self):
        stats = {}
        for book in self.books:
            stats[book.title] = {
                "author": book.author.name,
                "times_borrowed": book.times_borrowed,
                "return_rate": (book.total_returns / book.times_borrowed * 100) if book.times_borrowed else 0,
                "average_reading_time": str(book.total_reading_time / book.total_returns) if book.total_returns else "N/A"
            }
        return stats

    def export_statistics_json(self, filename):
        stats = self.generate_statistics()
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=4, ensure_ascii=False)

# Приклад використання
author = Author("Леся Українка")
book = Book("Лісова пісня", author)
user = User("Іван")

library = Library()
library.add_book(book)
library.borrow_book(book, user)
library.return_book(book, user)

print(library.generate_statistics())
library.export_statistics_json("stats.json")
