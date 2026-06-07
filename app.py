from pydantic import BaseModel

class Book(BaseModel):
    title: str
    author: str

my_book = Book(
    title='Atomic Habits',
    author='IDk'
)

print(f'Book: \n{my_book.title}, author: {my_book.author}')