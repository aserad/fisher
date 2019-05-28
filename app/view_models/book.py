# -*- encoding: utf-8 -*-


class BookViewModel:
    def __init__(self, book):
        self.title = book['title']
        self.isbn = book['isbn']
        self.publisher = book['publisher']
        self.pages = book['pages'] or ''
        self.author = '、'.join(book['author'])
        self.price = book['price']
        self.summary = book['summary'] or ''
        self.image = book['image']
        self.pubdate = book['pubdate']
        self.binding = book['binding']

    @property
    def intro(self):
        # intros = filter(lambda x: True if x else False, [self.author, self.publisher, self.price])
        intros = [item for item in [self.author, self.publisher, self.price] if item]
        return ' / '.join(intros)


class BookCollection:
    def __init__(self):
        self.total = 0
        self.books = []
        self.keyword = ''

    def fill(self, yushu_book, keyword):
        self.total = yushu_book.total
        self.books = [BookViewModel(book) for book in yushu_book.books]
        self.keyword = keyword


class _BookViewModel:

    @classmethod
    def package_single(cls, data, keyword):
        returned = {
            'books': [],
            'total': 0,
            'keyword': keyword,
        }
        if data:
            returned['total'] = 1
            returned['books'] = [cls.__cut_book_data(data)]
        return returned

    @classmethod
    def package_collection(cls, data, keyword):
        returned = {
            'books': [],
            'total': 0,
            'keyword': keyword,
        }
        if data:
            returned['total'] = len(data.get('total'))
            returned['books'] = [cls.__cut_book_data(book) for book in data.get('books')]
        return returned

    @classmethod
    def __cut_book_data(cls, data):
        book = dict(
            title=data.get('title'),
            publisher=data.get('publisher'),
            pages=data.get('pages') or '',
            author='、'.join(data.get('author')),
            price=data.get('price'),
            summary=data.get('summary') or '',
            image=data.get('image'),
        )
        return book
