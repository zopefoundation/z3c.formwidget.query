#!python
from setuptools import find_packages
from setuptools import setup


setup(
    name='z3c.formwidget.query',
    version='1.0.0',
    author="Zope Community",
    author_email="zope3-dev@zope.org",
    description="A source query widget for z3c.form.",
    long_description=(
        open('README.rst').read() + '\n\n' +
        open('CHANGES.rst').read()
    ),
    license="ZPL 2.1",
    keywords="zope zope3 z3c.form",
    url='https://github.com/zopefoundation/z3c.formwidget.query',
    zip_safe=False,
    packages=find_packages('src'),
    include_package_data=True,
    package_dir={'': 'src'},
    namespace_packages=['z3c', 'z3c.formwidget'],
    extras_require=dict(
        test=[
            'lxml',
            'z3c.form [test]',
            'zope.testing',
            'zope.testrunner',
        ]),
    install_requires=[
        'setuptools',
        'z3c.form>=3.2.10',
        'zope.interface',
        'zope.schema',
        'zope.component',
        'zope.i18nmessageid',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Zope :: 3',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Zope Public License',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',  # noqa: E501 line too long
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    entry_points='''
        [z3c.autoinclude.plugin]
        target = plone
    ''',
)
