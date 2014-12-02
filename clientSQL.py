#Creating a simple Client that insert some information in a Mongo client
# and then extract one acording to the author's name
#It is conected to the port 27017 of the localhost
import pymongo
import datetime

from pymongo import MongoClient


def sqlInsert():
    client = MongoClient('localhost', 27017)
    db = client.test_database
    posts = db.posts

    #Creating information to be stored in the database
    post = {"country": "Germany",
            "title": "Mike",
            "link": "My first blog post!",
            "author": "Xavier Benavides",
            "contentSnippet": "Hello 1!"}

    new_posts = [{"country": "Spain",
                  "title": "Bravo salvo al Barcelona en Mestalla",
                  "link": "http://www.sport.es/es/noticias/barca/bravo-salvo-barca-mestalla-3733912",
                  "author": "Xavier Benavides",
                  "contentSnippet": "El Barcelona gano en Mestalla gracias al gol de Busquets... y a las paradas de Claudio Bravo, que evito el gol valencianista en dos ocasiones..."},
                 {"country": "France",
                  "title": "Paul",
                  "link": "Another post!",
                  "author": "Xavier Benavides",
                  "contentSnippet": "Hello 3!"},
                 {"country": "Italy",
                  "title": "Paul",
                  "link": "MongoDB is fun",
                  "author": "Xavier Benavides",
                  "contentSnippet": "Nello 4!"}]

    #Inserting the information in the database
    post_id = posts.insert(post)
    #Inserting bulk of information
    posts.insert(new_posts)

    return post_id

def sqlPop(count):
    client = MongoClient('localhost', 27017)
    db = client.test_database
    posts = db.posts

    #Getting the information from the Database
    id = posts.find_one({"country": count})

    return id



