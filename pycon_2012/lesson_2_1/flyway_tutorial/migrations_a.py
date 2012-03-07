def content():

    from flyway import Migration

    class Version0(Migration):
        version = 0

        def up(self):
            collection = self.session.db['forum.forum']
            for doc in collection.find():
                doc['metadata'] = dict(
                    name=doc.pop('name'),
                    description=doc.pop('description'),
                    created=doc.pop('created'))
                collection.save(doc)

        def down(self):
            collection = self.session.db['forum.forum']
            for doc in collection.find():
                metadata = doc.pop('metadata')
                doc.update(
                    name=metadata['name'],
                    description=metadata['description'],
                    created=metadata['created'])
                collection.save(doc)

content()    
