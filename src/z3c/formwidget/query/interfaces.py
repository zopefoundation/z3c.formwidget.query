from zope.schema.interfaces import ISource, IVocabularyTokenized

class IQuerySource(ISource, IVocabularyTokenized):
    def search(query_string):
        """Return values that match query."""
