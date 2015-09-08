Overview
========

This package implements a widget that lets users enter a query and
select from the results.

The widget works with ``zope.schema.Choice``-fields supplying a query
source [1], optionally in conjunction with a collection field which
then allows multiple selections.

The easiest way to use the widget is to provide one of the following
as ``widgetFactory``:

* z3c.formwidget.query.widget.QuerySourceFieldRadioWidget
* z3c.formwidget.query.widget.QuerySourceFieldCheckboxWidget

------

[1] The source needs to implement ``IQuerySource`` as defined in this
package.
