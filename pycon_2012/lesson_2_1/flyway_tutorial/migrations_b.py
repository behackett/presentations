def content():
    from flyway import Migration

    class Version0(Migration):
        version=0
        def up(self):
            pass
        def down(self):
            pass
        def up_requires(self):
            yield ('a', self.version)
            for req in Migration.up_requires(self):
                yield req
        def down_requires(self):
            yield ('a', self.version)
            for req in Migration.down_requires(self):
                yield req

content()
