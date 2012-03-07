import ming
from ming import fs

from lesson_2_0 import model as M20

sess = M20.sess

Attachment = fs.filesystem(
    'forum.attachment', sess)

Attachment = fs.filesystem(
    'forum.attachment', sess,
    ming.Field('author', str))
    
Attachment = fs.filesystem(
    'forum.attachment', sess,
    ming.Field('metadata', dict(
            author=str)))
    
