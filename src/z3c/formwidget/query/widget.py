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
import z3c.form.term
import z3c.form.browser.radio
import z3c.form.browser.checkbox

from z3c.formwidget.query import MessageFactory as _

class QueryTerms(z3c.form.term.Terms):
    
    def __init__(self, context, request, form, field, widget, terms):
        self.context = context
        self.request = request
        self.form = form
        self.field = field
        self.widget = widget
        
        self.terms = SimpleVocabulary(terms)
            
class QuerySubForm(z3c.form.form.Form):
    zope.interface.implements(z3c.form.interfaces.ISubForm)
    css_class = 'querySelectSearch'

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

class QuerySourceRadioWidget(z3c.form.browser.radio.RadioWidget):
    """Query source widget that allows single selection."""
    
    _queryform = None
    _resultsform = None

    def isChecked(self, term):
        return term.value in self.selection or term.token in self.value

    @property
    def source(self):
        return self.field.source

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
        source = self.source

        if IContextSourceBinder.providedBy(source):
            source = source(self.context)

        assert ISource.providedBy(source)

        if query is not None:
            terms = set(source.search(query))
        else:
            terms = set()

        values = set([term.token for term in terms])
        tokens = set([term.value for term in terms])

        # Add current selection (a value) to terms
        selection = zope.component.getMultiAdapter(
            (self.context, self.field), z3c.form.interfaces.IDataManager).get()

        if not isinstance(selection, (tuple, set, list)):
            selection = (selection,)

        self.selection = selection

        for value in selection:
            if value and value not in values:
                terms.add(source.getTerm(value))

        # Add tokens in the request to terms
        request_values = self.request.get(self.name, [])
        if not isinstance(request_values, (tuple, set, list)):
            request_values = (request_values,)

        for token in request_values:
            if token and token not in tokens:
                terms.add(source.getTermByToken(token))

        # set terms
        self.terms = QueryTerms(self.context, self.request, self.form, self.field, self, terms)

        # filter on extracted data
        value = self.extract()
        if value is not z3c.form.interfaces.NOVALUE:
            self.selection = map(self.terms.getValue, value)

        # update widget
        self.updateQueryWidget()

    def updateQueryWidget(self):
        z3c.form.browser.radio.RadioWidget.update(self)

    def renderQueryWidget(self):
        return z3c.form.browser.radio.RadioWidget.render(self)
        
    def render(self):
        subform = self.subform
        if self.terms:
            return "\n".join((subform.render(), self.renderQueryWidget()))

        return subform.render()

    def __call__(self):
        self.update()
        return self.render()

class QuerySourceCheckboxWidget(
    QuerySourceRadioWidget, z3c.form.browser.checkbox.CheckBoxWidget):
    """Query source widget that allows multiple selections."""
    
    zope.interface.implementsOnly(z3c.form.interfaces.ICheckBoxWidget)

    @property
    def source(self):
        return self.field.value_type.source

    def updateQueryWidget(self):
        z3c.form.browser.checkbox.CheckBoxWidget.update(self)

    def renderQueryWidget(self):
        return z3c.form.browser.checkbox.CheckBoxWidget.render(self)

@zope.interface.implementer(z3c.form.interfaces.IFieldWidget)
def QuerySourceFieldRadioWidget(field, request):
    return z3c.form.widget.FieldWidget(field, QuerySourceRadioWidget(request))

@zope.interface.implementer(z3c.form.interfaces.IFieldWidget)
def QuerySourceFieldCheckboxWidget(field, request):
    return z3c.form.widget.FieldWidget(field, QuerySourceCheckboxWidget(request))
