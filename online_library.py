import sqlite3

# Path to the SQLite database used throughout the module
DB_PATH = "books.db"
cn = sqlite3.connect("books.db")
cur=cn.cursor()

class Authors:
    id: int = 0
    national_code: str = ""
    name: str = ""
    last_name: str = ""
    birthday: str = ""
    grade: str = ""
    def __init__(self, id, national_code, name, last_name, birthday, grade):
        self.id = id
        self.national_code = national_code
        self.name = name
        self.last_name = last_name
        self.birthday = birthday
        self.grade = grade
    def __str__(self):
        return f"authors:\n id:{self.id}, national_code:{self.national_code}, name:{self.name}, last_name:{self.last_name}, birthday:{self.birthday}, grade:{self.grade}"
    def __eq__(self, other):
        return self.id==other.id
class Translators:
    id: int = 10
    national_code: str = ""
    name: str = ""
    last_name: str = ""
    grade: str = ""
    def __init__(self, id, national_code, name, last_name, grade):
        self.id = id
        self.national_code = national_code
        self.name = name
        self.last_name = last_name
        self.grade = grade
    def __str__(self):
        return f"Translators:\n id:{self.id}, national_code:{self.national_code}, name:{self.name}, last_name:{self.last_name}, grade:{self.grade}"
    def __eq__(self, other):
        return self.id==other.id

class Esrb_ratings:
    id: int = 0
    esrb_name: str = ""
    def __init__(self, id, esrb_name):
        self.id = id
        self.esrb_name = esrb_name
    def __str__(self):
        return f"esrb_rating:\n id:{self.id}, esrb_name:{self.esrb_name}"
    def __eq__(self, other):
        return self.id==other.id

class Publishers:
    id: int = 0
    name: str = ""
    address: str = ""
    phone_number: str = ""
    fax_number: str = ""
    email: str = ""
    establish_date: str = ""
    def __init__(self, id, name, address, phone_number, fax_number, email, establish_date):
        self.id = id
        self.name = name
        self.address = address
        self.phone_number = phone_number
        self.fax_number = fax_number
        self.email = email
        self.establish_date = establish_date
    def __str__(self):
        return f"Publishers:\n id:{self.id}, name:{self.name}, address:{self.address}, phone_number:{self.phone_number}, fax_number:{self.fax_number}, email:{self.email}, establish_date:{self.establish_date}"
    def __eq__(self, other):
        return self.id==other.id
class Resources:
    id: int = 0
    title: str = ""
    type: str = ""
    establish_date: str = ""
    def __init__(self, id, title, type, establish_date):
        self.id = id
        self.title = title
        self.type = type
        self.establish_date = establish_date
    def __str__(self):
        return f"Resources:\n id:{self.id}, title:{self.title}, type:{self.type}, establish_date:{self.establish_date}"
    def __eq__(self, other):
        return self.id==other.id

class Genres:
    id: int = 0
    name: str = ""
    def __init__(self, id, name):
        self.id = id
        self.name = name
    def __str__(self):
        return f"Genres:\n id:{self.id}, name:{self.name}"
    def __eq__(self, other):
        return self.id==other.id

class Languages:
    id: int = 0
    name: str = ""
    def __init__(self, id, name):
        self.id = id
        self.name = name
    def __str__(self):
        return f"Languages:\n id:{self.id}, Name:{self.name}"
    def __eq__(self, other):
        return self.id==other.id
class Book:
    id:int=int()
    name:str=str()
    title:str=str()
    description:str=str()
    esrb_rating:Esrb_ratings=None
    publisher:Publishers=None
    resources:list[Resources]=list()
    authors:list[Authors]=list
    translators:list[Translators]=list()
    genreses:list[Genres]=list()
    languages:list[Languages]=list()

class BooksDataAdapter:
    @staticmethod
    def get_all()->list:
        books=[]
        boks=cur.execute("SELECT * FROM books").fetchall()
        data_nn=cur.execute("SELECT id,name,title,description,esrb_rating_id,publisher_id,author_id,translator_id,resource_id,language_id,genre_id FROM books INNER JOIN book_author ON books.id=book_author.book_id INNER JOIN book_translator ON book_author.book_id=book_translator.book_id INNER JOIN book_resource ON book_translator.book_id=book_resource.book_id INNER JOIN book_language ON book_resource.book_id=book_language.book_id INNER JOIN book_genre ON book_language.book_id=book_genre.book_id;").fetchall()
        resources=ResourcesDataAdapter.get_all()
        authors=AuthorsDataAdapter.get_all()
        translators=TranslatorsDataAdapter.get_all()
        genres=GenresDataAdapter.get_all()
        languages=LanguagesDataAdapter.get_all()
        for book in boks:
            res=[resource for id in set([dt[8] for dt in data_nn if dt[0]==book[0]]) for resource in resources if resource==id]
            aut=[author for id in set([dt[6] for dt in data_nn if dt[0]==book[0]]) for author in authors if author==id]
            tra=[translator for id in set([dt[7] for dt in data_nn if dt[0]==book[0]]) for translator in translators if translator==id]
            gen=[genre for id in set([dt[10] for dt in data_nn if dt[0]==book[0]]) for genre in genres if genre==id]
            lan=[language for id in set([dt[9] for dt in data_nn if dt[0]==book[0]]) for language in languages if language==id]

            books.append(Book(book[0],book[1],book[2],book[3],book[4],book[5],res,aut,tra,gen,lan))
        
        return books

class AuthorsDataAdapter:
    @staticmethod
    def get_all():
        result = []
        with sqlite3.connect(DB_PATH) as cn:
            cur = cn.cursor()
            rows = cur.execute("SELECT id, national_code, name, last_name, birthday, grade FROM authors").fetchall()
            for row in rows:
                result.append(Authors(row[0], row[1], row[2], row[3], row[4], row[5]))
        return result

    @staticmethod
    def insert(authors: Authors):
        with sqlite3.connect(DB_PATH) as cn:
            cur = cn.cursor()
            cur.execute(
                "INSERT INTO authors (national_code, name, last_name, birthday, grade) VALUES (?, ?, ?, ?, ?)",
                (authors.national_code, authors.name, authors.last_name, authors.birthday, authors.grade),
            )
            cn.commit()
            authors.id = cur.lastrowid
        return authors
    @staticmethod
    def delete(id:int):
        with sqlite3.connect(DB_PATH) as cn:
            cur = cn.cursor()
            # Check if the author id is referenced in books table
            ref = cur.execute("SELECT 1 FROM books WHERE author = ? LIMIT 1", (id,)).fetchone()
            if ref is None:
                cur.execute("DELETE FROM authors WHERE id = ?", (id,))
                cn.commit()
                return True
            return False
class TranslatorsDataAdapter:
    @staticmethod
    def get_all():
        result = []
        with sqlite3.connect(DB_PATH) as cn:
            cur = cn.cursor()
            rows = cur.execute("SELECT id, national_code, name, last_name, grade FROM translators").fetchall()
            for row in rows:
                result.append(Translators(row[0], row[1], row[2], row[3], row[4]))
        return result

    @staticmethod
    def insert(translators: Translators):
        with sqlite3.connect(DB_PATH) as cn:
            cur = cn.cursor()
            cur.execute(
                "INSERT INTO translators (national_code, name, last_name, grade) VALUES (?, ?, ?, ?)",
                (translators.national_code, translators.name, translators.last_name, translators.grade),
            )
            cn.commit()
            translators.id = cur.lastrowid
        return translators
    @staticmethod
    def delete (id:int):
        with sqlite3.connect(DB_PATH) as cn:
            cur = cn.cursor()
            ref = cur.execute("SELECT 1 FROM books WHERE translator = ? LIMIT 1", (id,)).fetchone()
            if ref is None:
                cur.execute("DELETE FROM translators WHERE id = ?", (id,))
                cn.commit()
                return True
            return False

class Esrb_ratingsDataAdapter:
    @staticmethod
    def get_all():
        result = []
        with sqlite3.connect(DB_PATH) as cn:
            cur = cn.cursor()
            rows = cur.execute("SELECT id, esrb_name FROM esrb_ratings").fetchall()
            for row in rows:
                result.append(Esrb_ratings(row[0], row[1]))
        return result

    @staticmethod
    def insert(esrb_ratings: Esrb_ratings):
        with sqlite3.connect(DB_PATH) as cn:
            cur = cn.cursor()
            cur.execute("INSERT INTO esrb_ratings (esrb_name) VALUES (?)", (esrb_ratings.esrb_name,))
            cn.commit()
            esrb_ratings.id = cur.lastrowid
        return esrb_ratings
    @staticmethod
    def delete (id:int):
        with sqlite3.connect(DB_PATH) as cn:
            cur = cn.cursor()
            ref = cur.execute("SELECT 1 FROM books WHERE esrb_rating = ? LIMIT 1", (id,)).fetchone()
            if ref is None:
                cur.execute("DELETE FROM esrb_ratings WHERE id = ?", (id,))
                cn.commit()
                return True
            return False
class PublishersDataAdapter:
    @staticmethod
    def get_all():
        result = []
        with sqlite3.connect(DB_PATH) as cn:
            cur = cn.cursor()
            rows = cur.execute("SELECT id, name, address, phone_number, fax_number, email, establish_date FROM publishers").fetchall()
            for row in rows:
                result.append(Publishers(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))
        return result

    @staticmethod
    def insert(publishers: Publishers):
        with sqlite3.connect(DB_PATH) as cn:
            cur = cn.cursor()
            cur.execute(
                "INSERT INTO publishers (name, address, phone_number, fax_number, email, establish_date) VALUES (?, ?, ?, ?, ?, ?)",
                (publishers.name, publishers.address, publishers.phone_number, publishers.fax_number, publishers.email, publishers.establish_date),
            )
            cn.commit()
            publishers.id = cur.lastrowid
        return publishers
    @staticmethod
    def delete (id:int):
        with sqlite3.connect(DB_PATH) as cn:
            cur = cn.cursor()
            ref = cur.execute("SELECT publisher_id FROM books")
            if ref is None:
                cur.execute(f"DELETE FROM publishers where id={id}")
                cn.commit()
                return True
            return False

class ResourcesDataAdapter:
    @staticmethod
    def get_all():
        result = []
        with sqlite3.connect(DB_PATH) as cn:
            cur = cn.cursor()
            rows = cur.execute("SELECT id, title, type, establish_date FROM resources").fetchall()
            for row in rows:
                result.append(Resources(row[0], row[1], row[2], row[3]))
        return result

    @staticmethod
    def insert(resources: Resources):    
        with sqlite3.connect(DB_PATH) as cn:
            cur = cn.cursor()
            cur.execute(
                "INSERT INTO resources (title, type, establish_date) VALUES (?, ?, ?)",
                (resources.title, resources.type, resources.establish_date),
            )
            cn.commit()
            resources.id = cur.lastrowid
        return resources
    @staticmethod
    def delete (id:int):
        with sqlite3.connect(DB_PATH) as cn:
            cur = cn.cursor()
            ref = cur.execute("SELECT 1 FROM books WHERE resource = ? LIMIT 1", (id,)).fetchone()
            if ref is None:
                cur.execute("DELETE FROM resources WHERE id = ?", (id,))
                cn.commit()
                return True
            return False
class GenresDataAdapter:
    @staticmethod
    def get_all():
        result = []
        with sqlite3.connect(DB_PATH) as cn:
            cur = cn.cursor()
            rows = cur.execute("SELECT id, name FROM genres").fetchall()
            for row in rows:
                result.append(Genres(row[0], row[1]))
        return result

    @staticmethod
    def insert(genres: Genres):
        with sqlite3.connect(DB_PATH) as cn:
            cur = cn.cursor()
            cur.execute("INSERT INTO genres (name) VALUES (?)", (genres.name,))
            cn.commit()
            genres.id = cur.lastrowid
        return genres
    @staticmethod
    def delete (id:int):
        with sqlite3.connect(DB_PATH) as cn:
            cur = cn.cursor()
            ref = cur.execute("SELECT 1 FROM books_genres WHERE genre = ? LIMIT 1", (id,)).fetchone()
            if ref is None:
                cur.execute("DELETE FROM genres WHERE id = ?", (id,))
                cn.commit()
                return True
            return False

class LanguagesDataAdapter:
    @staticmethod
    def get_all():
        result = []
        with sqlite3.connect(DB_PATH) as cn:
            cur = cn.cursor()
            rows = cur.execute("SELECT id, name FROM languages").fetchall()
            for row in rows:
                result.append(Languages(row[0], row[1]))
        return result

    @staticmethod
    def insert(languages: Languages):
        with sqlite3.connect(DB_PATH) as cn:
            cur = cn.cursor()
            cur.execute("INSERT INTO languages (name) VALUES (?)", (languages.name,))
            cn.commit()
            languages.id = cur.lastrowid
        return languages
    @staticmethod
    def delete (id:int):
        with sqlite3.connect(DB_PATH) as cn:
            cur = cn.cursor()
            ref = cur.execute("SELECT 1 FROM books WHERE language = ? LIMIT 1", (id,)).fetchone()
            if ref is None:
                cur.execute("DELETE FROM languages WHERE id = ?", (id,))
                cn.commit()
                return True
            return False


authors_list = AuthorsDataAdapter.get_all()
translators_list = TranslatorsDataAdapter.get_all()
esrb_list = Esrb_ratingsDataAdapter.get_all()
publishers_list = PublishersDataAdapter.get_all()
resources_list = ResourcesDataAdapter.get_all()
genres_list = GenresDataAdapter.get_all()
languages_list = LanguagesDataAdapter.get_all()
for book in BooksDataAdapter.get_all():
    print(book)
# for author in authors_list:
#     print(author)
# for translator in translators_list:
#     print(translator)
# for esrb in esrb_list:
#     print(esrb)
# for publisher in publishers_list:
#     print(publisher)
# for resource in resources_list:
#     print(resource)
# for genre in genres_list:
#     print(genre)
# for language in languages_list:
#     print(language)

p1 = Languages(0, "English")
inserted_publisher = LanguagesDataAdapter.insert(p1)
print("After Insert Languages:")
print(inserted_publisher)
a1 = Authors(0, "1234567890", "John", "Doe", "1980-01-01", "A")
inserted_author = AuthorsDataAdapter.insert(a1)
print("After Insert Authors:")
print(inserted_author)
t1 = Translators(0, "0987654321", "Jane", "Smith", "B")
inserted_translator = TranslatorsDataAdapter.insert(t1)
print("After Insert Translators:")
print(inserted_translator)
e1 = Esrb_ratings(0, "Everyone")
inserted_esrb = Esrb_ratingsDataAdapter.insert(e1)
print("After Insert Esrb_ratings:")
print(inserted_esrb)