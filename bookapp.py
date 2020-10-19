# import re
import traceback
from bookdb import BookDB

DB = BookDB()


def book(book_id):
    # return "<h1>a book with id %s</h1>" % book_id
    # return f'Specific book with id {book_id}'
#     page = """
# <h1>{title}</h1>
# <table>
#     <tr><th>Author</th><td>{author}</td></tr>
#     <tr><th>Publisher</th><td>{publisher}</td></tr>
#     <tr><th>ISBN</th><td>{isbn}</td></tr>
# </table>
# <a href="/">Back to the list</a>
# """
#     book = DB.title_info(book_id)
#     if book is None:
#         raise NameError
#     return page.format(**book)
    book = DB.title_info(book_id)
    if book is None:
        raise NameError
    page = f'''
<h1>{book['title']}</h1>
<table>
    <tr><th>Author</th><td>{book['author']}</td></tr>
    <tr><th>Publisher</th><td>{book['publisher']}</td></tr>
    <tr><th>ISBN</th><td>{book['isbn']}</td></tr>
</table>
<a href="/">Back to the list</a>
'''
    return page

def books():
    # return "<h1>a list of books</h1>"
    all_books = DB.titles()
    body = ['<h1>My Bookshelf</h1>', '<ul>']
    item_template = '<li><a href="/book/{id}">{title}</a></li>'
    for book in all_books:
        body.append(item_template.format(**book))
    body.append('</ul>')
    return '\n'.join(body)

def resolve_path(path):
    funcs = {'': books,
             'book': book,
             }
    path = path.strip('/').split('/')
    func_name = path[0]
    args = path[1:]
    try:
        func = funcs[func_name]
    except KeyError:
        raise NameError
    return func, args

def application(environ, start_response):
    # status = "200 OK"
    headers = [('Content-type', 'text/html')]
    try:
        path = environ.get('PATH_INFO', None)
        print(path)
        if path is None:
            raise NameError
        func, args = resolve_path(path)
        status = '200 OK'
        body = func(*args)
    except NameError:
        status = '404 Not Found'
        body = '<h1>Not Found</h1>'
    except Exception:
        status = '500 Internal Server Error'
        body = '<h1>Internal Server Error</h1>'
        print(traceback.format_exc())
    finally:
        headers.append(('Content-type', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]
    # return ["<h1>No Progress Yet</h1>".encode('utf8')]


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
