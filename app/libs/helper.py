# -*- encoding: utf-8 -*-

import re


def is_isbn_or_key(word):
    """判断是isbn还是关键字"""
    # isbn isbn13  13个0到9的数字组成
    #      isbn10  10个0到9的数字组成，含有一些 '-'
    isbn_or_key = 'key'
    if re.match('^\d{13}$', word):
        isbn_or_key = 'isbn'
    if '-' in word and re.match('^\d{10}$', word.replace('-', '')):
        isbn_or_key = 'isbn'
    
    return isbn_or_key
