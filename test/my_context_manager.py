# -*- encoding: utf-8 -*-

from contextlib import contextmanager


class MyResource:
    # def __enter__(self):
    #     print("connect to resource")
    #     return self
    #
    # def __exit__(self, exc_type, exc_val, exc_tb):
    #     print('close resource connection')

    def query(self):
        print('query data')


@contextmanager
def make_my_resource():
    print("connect to resource")
    yield MyResource()
    print('close resource connection')


def main():
    with make_my_resource() as res:
        res.query()


if __name__ == '__main__':
    main()
