import json
from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked
import os
import math
import glob

def on_reload():
    os.makedirs('pages', exist_ok=True)

    library_pages = list(chunked(books_information, 20))
    library_pages_filepaths = set()

    for index, library_page in enumerate(library_pages):
        paired_books = list(chunked(library_page, 2))
        page_filepath = 'pages/index{}.html'.format(index + 1)
        page_renderer(index, paired_books, page_filepath)

        library_pages_filepaths.add(page_filepath)

    remove_unused_pages(library_pages_filepaths)

    print("Site rebuilded")



def page_renderer(index, paired_books,page_filepath):
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    rendered_page = template.render(
        paired_books=paired_books,
        pages_amount=math.ceil(len(books_information)/20),
        current_page_number=index+1,
    )

    with open(page_filepath, 'w', encoding="utf8") as file:
        file.write(rendered_page)


def remove_unused_pages(library_pages_filepaths):
    pages_folder_content = set(glob.glob('pages/*.html'))
    pages_for_removing = pages_folder_content.difference(library_pages_filepaths)
    for page in pages_for_removing:
        os.remove(page)

if __name__ == '__main__':
    with open('books_information.json', 'r') as json_file:
        books_json = json_file.read()

    books_information = json.loads(books_json)

    on_reload()

    server = Server()
    server.watch('template.html', on_reload())
    server.serve(root='./pages/')