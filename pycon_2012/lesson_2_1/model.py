from datetime import datetime

import ming

from lesson_2_0 import model as M20

sess = M20.sess

def migrate_forum(doc):
    metadata = dict(
        name=doc.pop('name'),
        description=doc.pop('description'),
        created=doc.pop('created'))
    return dict(doc, metadata=metadata)

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
    ming.Field('num_posts', int),
    version_of=M20.Forum,
    migrate=migrate_forum)

# Clear the database and put an 'old' forum document in
M20.Forum.m.remove()
M20.Forum.make(dict(name='My Forum')).m.insert()

def migrate_forum(doc):
    metadata = dict(
        name=doc.pop('name'),
        description=doc.pop('description'),
        created=doc.pop('created'))
    return dict(doc, metadata=metadata, version=2)

Forum = ming.collection(
    'forum.forum', sess, 
    ming.Field('_id', ming.schema.ObjectId),
    ming.Field('metadata', dict(
            name=str,
            description=str,
            created=ming.schema.DateTime(if_missing=datetime.utcnow))),
    ming.Field('last_post', dict(
            when=datetime,
            user=str,
            subject=str)),
    ming.Field('num_threads', int),
    ming.Field('num_posts', int),
    ming.Field('schema_version', ming.schema.Value(2, required=True)),
    version_of=M20.Forum,
    migrate=migrate_forum)
