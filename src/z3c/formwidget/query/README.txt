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

To make things simple, we'll just use unicode strings as values.

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
  ...     getTerm = vocabulary.getTerm
  ...     getTermByToken = vocabulary.getTermByToken
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

Widgets
-------

There are two widgets available; one that corresponds to a single
selection or a multi-selection of items from the source.

To enable multiple selections, wrap the ``zope.schema.Choice`` in a field
derived from ``zope.schema.Collection``.

Let's begin with a single selection.

  >>> class Location(object):
  ...     city = None
  
  >>> location = Location()

  >>> from z3c.formwidget.query.widget import QuerySourceFieldRadioWidget

  >>> def setupWidget(field, context, request):
  ...     widget = QuerySourceFieldRadioWidget(field, request)
  ...     widget.name = field.__name__
  ...     widget.context = context
  ...     return widget

  >>> from z3c.form.testing import TestRequest
  >>> request = TestRequest()

An empty query is not carried out.
  
  >>> widget = setupWidget(city, location, request)
  >>> 'type="radio"' in widget()
  False

Let's choose a city:

  >>> location.city = u"Palermo"

  >>> widget = setupWidget(city, location, request)

We now expect a radio button to be present.
  
  >>> 'type="radio"' in widget()
  True
  
We can put a query string in the request, and have our source queried.

  >>> request = TestRequest(form={
  ...     'city.widgets.query': u'bologna'})
  
  >>> widget = setupWidget(city, location, request)

Verify results:
  
  >>> 'Bologna' in widget()
  True

  >>> 'Sorrento' in widget()
  False

Selecting 'Bologna' from the list should check the corresponding box.

  >>> request = TestRequest(form={
  ...     'city.widgets.query': u'bologna',
  ...     'city': ('bologna',)})

  >>> widget = setupWidget(city, location, request)

  >>> 'checked="checked"' in widget()
  True

Now we want to try out selection of multiple items.

  >>> cities = zope.schema.Set(
  ...     __name__='cities',
  ...     title=u'Cities',
  ...     description=u'Select one or more cities.',
  ...     value_type=zope.schema.Choice(
  ...         source=ItalianCitiesSourceBinder()
  ...     ))

  >>> class Route(object):
  ...     cities = ()
  
  >>> route = Route()

  >>> from z3c.formwidget.query.widget import QuerySourceFieldCheckboxWidget

  >>> def setupMultiWidget(field, context, request):
  ...     widget = QuerySourceFieldCheckboxWidget(field, request)
  ...     widget.name = field.__name__
  ...     widget.context = context
  ...     return widget

  >>> request = TestRequest()
  
An empty query is not carried out.
  
  >>> widget = setupMultiWidget(cities, route, request)
  >>> 'type="checkbox"' in widget()
  False

Let's set a city on the route:

  >>> route.cities = (u"Palermo",)

  >>> widget = setupMultiWidget(cities, route, request)
  >>> 'type="checkbox"' in widget()
  True
  
Let's make a query for "bologna".

  >>> request = TestRequest(form={
  ...     'cities.widgets.query': u'bologna'})
  
  >>> widget = setupMultiWidget(cities, route, request)

Verify results:

  >>> 'Bologna' in widget()
  True

  >>> 'Sorrento' in widget()
  False

We'll select 'Bologna' from the list.

  >>> request = TestRequest(form={
  ...     'cities.widgets.query': u'bologna',
  ...     'cities': ('bologna',)})

  >>> widget = setupMultiWidget(cities, route, request)

Verify that Bologna has been selected.

  >>> 'checked="checked"' in widget()
  True

Let's try and simulate removing the item we've set on the
context. We'll submit an empty tuple.

  >>> request = TestRequest(form={
  ...     'cities': ()})

  >>> widget = setupMultiWidget(cities, route, request)

We expect an unchecked box.

  >>> 'type="checkbox"' in widget()
  True
  
  >>> 'checked="checked"' in widget()
  False

Named Sources
-------------

We can also provide a data source using named vocabularies.  First we register
our source as a named vocabulary::

  >>> from zope.schema.interfaces import IVocabularyFactory
  >>> from zope.schema.vocabulary import getVocabularyRegistry
  >>> vr = getVocabularyRegistry()
  >>> vr.register(u'test vocabulary name', ItalianCities)
  >>> city2 = zope.schema.Choice(
  ...     __name__='city',
  ...     title=u'City',
  ...     description=u'Select a city.',
  ...     vocabulary=u'test vocabulary name')
  >>> request = TestRequest(form={
  ...     'city.widgets.query': u'bologna',
  ...     'city': ('bologna',)})
  >>> location = Location()
  >>> widget = setupWidget(city2, location, request)
  >>> 'Bologna' in widget()
  True
  >>> 'Palermo' in widget()
  False

The same is true of multi-select widgets::

  >>> cities2 = zope.schema.Set(
  ...     __name__='cities',
  ...     title=u'Cities',
  ...     description=u'Select one or more cities.',
  ...     value_type=zope.schema.Choice(
  ...        vocabulary=u'test vocabulary name' 
  ...     ))
  >>> route = Route()
  >>> request = TestRequest(form={
  ...     'cities.widgets.query': u'bologna',
  ...     'cities': ('bologna',)})
  >>> widget = setupMultiWidget(cities2, route, request)
  >>> 'Bologna' in widget()
  True
  >>> 'Palermo' in widget()
  False


Todo
----

- Functional testing with zope.testbrowser
