Changelog
=========


0.13 (2017-01-17)
-----------------

- Compatible with z3c.form > 3.2.10, where radio and checkbox `items` property is a generator.
  [thomasdesvenain]


0.12 (2015-09-09)
-----------------

- Code moved to https://github.com/zopefoundation/z3c.formwidget.query
  [maurits]


0.11 (2015-04-29)
-----------------

- Get default value from IValue adapter.
  [vincentfretin]


0.10 (2014-02-19)
-----------------

- Remove :list from novalue radio box name to be the same behavior
  as z3c.form >= 2.6.0.
  [vincentfretin]


0.9 (2012-08-30)
----------------

* Avoid test dependency on zope.app.testing.
  [hannosch]

* Remove unused dependency on zope.app.form.
  [hannosch]


0.8 (2012-02-20)
----------------

* If one of the values to be displayed provides IRoleManager,
  then check for permission first.
  [frapell]


0.7 (2011-11-07)
----------------

* Use an ordered list instead of a set to represent source items.
  [timo]


0.6 (2011-05-04)
----------------

* Add an ignoreMissing parameter and widget subclasses to avoid errors when
  rendering missing values.
  [elro]

* Create changelog file.
  [dukebody]

* Respect the ignoreRequest parameter.
  [dukebody]


0.5 (2009-04-17)
----------------

* ...


0.3 (2008-08-28)
----------------

* ...
