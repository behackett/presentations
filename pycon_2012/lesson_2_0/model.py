import ming
from ming.datastore import DataStore
from datetime import datetime

ds = DataStore('mongodb://localhost:27017', database='tutorial')
sess = ming.Session(ds)

Forum = ming.collection(
    'forum.forum', sess, 
    ming.Field('_id', ming.schema.ObjectId),
    ming.Field('name', str),
    ming.Field('description', str),
    ming.Field('created', datetime, if_missing=datetime.utcnow),
    ming.Field('last_post', dict(
        when=datetime,
        user=str,
        subject=str)),
    ming.Field('num_threads', int),
    ming.Field('num_posts', int))

Thread = ming.collection(
    'forum.thread', sess,
    ming.Field('_id', ming.schema.ObjectId),
    ming.Field(
        'forum_id', ming.schema.ObjectId(if_missing=None),
        index=True),
    ming.Field('subject', str),
    ming.Field('last_post', dict(
        when=datetime,
        user=str,
        subject=str)),
    ming.Field('num_posts', int))

Post = ming.collection(
    'forum.post', sess,
    ming.Field('_id', ming.schema.ObjectId),
    ming.Field('subject', str),
    ming.Field('forum_id', ming.schema.ObjectId(if_missing=None)),
    ming.Field('thread_id', ming.schema.ObjectId(if_missing=None)),
    ming.Field('parent_id', ming.schema.ObjectId(if_missing=None)),
    ming.Field('timestamp', datetime, if_missing=datetime.utcnow),
    ming.Field('slug', str),
    ming.Field('fullslug', str, unique=True),
    ming.Index([('forum_id', 1), ('thread_id', 1)]),
    ming.Index('slug', unique=True))

# Create hierarchy
Product = ming.collection(
    'product', sess,
    ming.Field('_id', str), # sku
    ming.Field('category', str, if_missing='product'),
    ming.Field('name', str),
    ming.Field('price', int), # in cents
    polymorphic_on='category',
    polymorphic_identity='base')
    
Shirt = ming.collection(
    Product, 
    ming.Field('category', str, if_missing='shirt'),
    ming.Field('size', str),
    polymorphic_identity='shirt')
    
Film = ming.collection(
    Product,
    ming.Field('category', str, if_missing='film'),
    ming.Field('genre', str),
    polymorphic_identity='film')
