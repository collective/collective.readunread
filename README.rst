Introduction
============

This package provides read/unread status for Plone objects.

It adds a "readBy" field and a proper index to any object marked with IReadByProvider interface.


How to use
==========

Just add a ZCML slug in your package like::

    <five:implements
      class="Products.ATContentTypes.content.document.ATDocument"
      interface="collective.readunread.interfaces.IReadByProvider"
      />


Credits
=======

Developed with the support of `International Traning Center of the ILO`__.

.. image:: http://www.itcilo.org/logo_en.jpg
   :alt: ITCILO - Logo
   :target: http://www.itcilo.org/

__ http://www.itcilo.org/


Authors
=======

This product was developed by Domsense.

.. image:: http://domsense.com/logo-txt.png
   :alt: Domsense Website
   :target: http://www.domsense.com/
