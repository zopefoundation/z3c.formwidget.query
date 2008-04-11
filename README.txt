Overview
========

This package implements a widget that lets users enter a query and
select from the results.

The widget currently works with ``zope.schema.Choice``-fields
supplying a query source [1].

Results need to implement or adapt to ``ITitledTokenizedTerm``.

------

[1] The source needs to implement ``IQuerySource`` as defined in this
package.
