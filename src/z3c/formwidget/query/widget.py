import zope.component
import zope.interface
import zope.schema
import zope.schema.interfaces

from zope.app.form.browser.interfaces import ITerms
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.interfaces import ITitledTokenizedTerm
from zope.schema.interfaces import ISource, IContextSourceBinder

import z3c.form.interfaces
import z3c.form.button
import z3c.form.form
import z3c.form.field
import z3c.form.widget
import z3c.form.browser.radio

from z3c.formwidget.query import MessageFactory as _

class QueryTerms(SimpleVocabulary):
    zope.interface.implements(ITerms)
    
    def __init__(self, values):
        terms = [ITitledTokenizedTerm.providedBy(value) and value or \
                 ITitledTokenizedTerm(value) for value in values]

        super(QueryTerms, self).__init__(terms)

    def getTerm(self, value):
        try:
            return self.by_value[value]
        except KeyError:
            raise LookupError(value)

    def getValue(self, token):
        try:
            return self.by_token[token]
        except KeyError:
            raise LookupError(token)

class QuerySubForm(z3c.form.form.Form):
    zope.interface.implements(z3c.form.interfaces.ISubForm)

    fields = z3c.form.field.Fields(
        zope.schema.TextLine(
        __name__='query',
        required=False))

    def __init__(self, context, request, prefix=None):
        super(QuerySubForm, self).__init__(context, request)

        if prefix is not None:
            self.prefix = prefix    

    @z3c.form.button.buttonAndHandler(_(u"Search"))
    def search(self, action):
        data, errors = self.widgets.extract()
        if not errors:
            z3c.form.form.applyChanges(self, self.context, data)

class QueryContext(object):
    query = None

class QuerySourceWidget(z3c.form.browser.radio.RadioWidget):
    _queryform = None
    _resultsform = None

    def update(self):
        # setup query form
        prefix = self.name
        
        subform = self.subform = QuerySubForm(QueryContext(), self.request, prefix)
        subform.update()

        data, errors = subform.extractData()
        if errors:
            return

        # query source
        query = data['query']
        source = self.field.source

        if IContextSourceBinder.providedBy(source):
            source = source(self.context)

        assert ISource.providedBy(source)

        if query is not None:
            results = source.search(query)
        else:
            results = ()
            
        # set terms
        self.terms = QueryTerms(results)

                # update widget
        super(QuerySourceWidget, self).update()
        
    def render(self):
        subform = self.subform
        if self.terms:
            return "\n".join((subform.render(), super(QuerySourceWidget, self).render()))

        return subform.render()

    def __call__(self):
        self.update()
        return self.render()
    
@zope.component.adapter(zope.schema.interfaces.IChoice, z3c.form.interfaces.IFormLayer)
@zope.interface.implementer(z3c.form.interfaces.IFieldWidget)
def QuerySourceFieldWidget(field, request):
    return z3c.form.widget.FieldWidget(field, QuerySourceWidget(request))
