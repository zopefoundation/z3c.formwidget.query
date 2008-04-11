z3c.formwidget.query
====================

This package provides a widget to query a source.

  >>> from z3c.form import testing
  >>> testing.setupFormDefaults()

We must register a form page template to render forms.

  >>> from z3c.form import form, testing
  >>> factory = form.FormTemplateFactory(
  ...     testing.getPath('../tests/simple_subedit.pt'))

Let's register our new template-based adapter factory:

  >>> component.provideAdapter(factory)

Sources
-------

Let's start by defining a source.

  >>> from z3c.formwidget.query.interfaces import IQuerySource
  >>> from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

  >>> class ItalianCities(object):
  ...     interface.implements(IQuerySource)
  ...
  ...     vocabulary = SimpleVocabulary((
  ...         SimpleTerm(u'Bologna', 'bologna', u'Bologna'),
  ...         SimpleTerm(u'Palermo', 'palermo', u'Palermo'),
  ...         SimpleTerm(u'Sorrento', 'sorrento', u'Sorrento')))
  ...
  ...     def __init__(self, context):
  ...         self.context = context
  ...
  ...     __contains__ = vocabulary.__contains__
  ...     __iter__ = vocabulary.__iter__
  ...
  ...     def search(self, query_string):
  ...         return [v for v in self if query_string.lower() in v.value.lower()]

  >>> from zope.schema.interfaces import IContextSourceBinder

  >>> class ItalianCitiesSourceBinder(object):
  ...     interface.implements(IContextSourceBinder)
  ...
  ...     def __call__(self, context):
  ...         return ItalianCities(context)
  
Fields setup
------------

  >>> import zope.component
  >>> import zope.schema
  >>> import zope.app.form.browser
  >>> from zope.publisher.interfaces.browser import IBrowserRequest

First we have to create a field and a request:

  >>> city = zope.schema.Choice(
  ...     __name__='city',
  ...     title=u'City',
  ...     description=u'Select a city.',
  ...     source=ItalianCitiesSourceBinder())

Widget
------

  >>> class Content(object):
  ...     city = None
  
  >>> content = Content()
  >>> field = city.bind(content)

  >>> from z3c.formwidget.query.widget import QuerySourceFieldWidget

  >>> def setupWidget(field, context, request):
  ...     widget = QuerySourceFieldWidget(field, request)
  ...     widget.name = field.__name__
  ...     return widget

  >>> from z3c.form.testing import TestRequest
  >>> request = TestRequest()

An empty query is not carried out.
  
  >>> widget = setupWidget(field, content, request)
  
  >>> 'type="radio"' in widget()
  False

Let's make a query for "bologna".

  >>> request = TestRequest(form={
  ...     'city.widgets.query': u'bologna'})
  
  >>> widget = setupWidget(field, content, request)

Verify results:
  
  >>> 'Bologna' in widget()
  True

  >>> 'Sorrento' in widget()
  False

We'll select 'Bologna' from the list.

  >>> request = TestRequest(form={
  ...     'city.widgets.query': u'bologna',
  ...     'city': ('bologna',)})

  >>> widget = setupWidget(field, content, request)

Verify that Bologna has been selected.

  >>> 'checked="checked"' in widget()
  True

Todo
----

- Functional testing with zope.testbrowser
