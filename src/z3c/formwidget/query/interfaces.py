from zope.schema.interfaces import ISource

class IQuerySource(ISource):
    def search(query_string):
        """Return values that match query."""
