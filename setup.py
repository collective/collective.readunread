from setuptools import setup, find_packages
import os

version = '1.0b5'

def get_long_desc():
    contents = [
        open(os.path.join("collective","readunread","README.rst")).read(),
        open(os.path.join("docs", "HISTORY.txt")).read(),
        open(os.path.join("docs", "CREDITS.txt")).read(),
    ]
    return "\n".join(contents)

setup(name='collective.readunread',
      version=version,
      description="",
      long_description=get_long_desc(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='Plone',
      author='Simone Orsi',
      author_email='simahawk@gmail.com',
      url='https://github.com/collective/collective.readunread',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'plone.validatehook',
          'archetypes.schemaextender',
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      setup_requires=["PasteScript"],
      paster_plugins=["ZopeSkel"],
      )
