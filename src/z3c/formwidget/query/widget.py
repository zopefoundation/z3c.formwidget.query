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
import z3c.form.browser.checkbox

from z3c.formwidget.query import MessageFactory as _

class QueryTerms(SimpleVocabulary):
    zope.interface.implements(ITerms)
    
    def __init__(self, terms):
        super(QueryTerms, self).__init__(terms)

    def getTerm(self, value):
        return self.by_value[value]
        
    def getValue(self, token):
        return self.by_token[token].value
        
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

        # add current selection
        selection = zope.component.getMultiAdapter(
            (self.context, self.field), z3c.form.interfaces.IDataManager).get()

        if not isinstance(selection, (tuple, set, list)):
            selection = (selection,)

        values = [term.value for term in terms]

        map(terms.add,
            map(source.getTermByValue,
                filter(lambda value: value and value not in values, selection)))
        
        self.selection = selection

        # set terms
        self.terms = QueryTerms(terms)

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
