from ming.odm import ThreadLocalODMSession, Mapper
from ming.odm import ForeignIdProperty, RelationProperty

from lesson_2_0 import model as M

sess = ThreadLocalODMSession(M.sess)

class Forum(object):
    pass

class Thread(object):
    pass

class Post(object):
    pass

sess.mapper(Forum, M.Forum, properties=dict(
        threads=RelationProperty('Thread')))
sess.mapper(Thread, M.Thread, properties=dict(
        forum_id=ForeignIdProperty('Forum'),
        forum=RelationProperty('Forum'),
        posts=RelationProperty('Post')))
sess.mapper(Post, M.Post, properties=dict(
        forum_id=ForeignIdProperty('Forum'),
        thread_id=ForeignIdProperty('Thread'),
        forum=RelationProperty('Forum'),
        thread=RelationProperty('Thread')))

Mapper.compile_all()

class Product(object):
    pass

class Shirt(Product):
    pass

class Film(Product):
    pass

sess.mapper(Product, M.Product,
            polymorphic_on='category',
            polymorphic_identity='base')
sess.mapper(Shirt, M.Shirt,
            polymorphic_identity='shirt')
sess.mapper(Film, M.Film,
            polymorphic_identity='film')

Mapper.compile_all()
