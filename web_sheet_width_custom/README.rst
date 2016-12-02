
.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

======================
Web Sheet Width Custom
======================

This module adds a css class to change a Form Sheet view
to cover the full screen.

You can apply this css class either in the arch xml view 
either by configuration in the view form.


Configuration
=============

To configure this module, you need to:

#. Apply 'Technical Features' rights to your user

#. Go to the form view of your choice with the menu
   (Settings > Technical > User Interface > Views)

#. Apply a value in the 'Form Width' field.

.. figure:: web_sheet_width_custom/static/description/img1.png
   :alt: Set full width
   :width: 600 px

|

Alternative way is to define the css class directly in your view.

You can activate the Full Screen view by the creation of an
inherited view with the following content:
::

    <xpath expr="//sheet" position="attributes">
        <attribute name="class">oe_form_sheet_full_screen</attribute>
    </xpath>


Install the 'web_sheet_full_width' module if you want to have a full screen
behaviour in all sheets.


Usage
=====

To use this module, you need to configure the form view of your choice 
as explained above.



Known issues / Roadmap
======================

* add other css styles to have more choice on width.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/akretion/odoo-usability/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smashing it by providing a detailed and welcomed feedback.

Credits
=======

Images
------

Icon courtesy of http://www.picol.org/ (size_width.svg)


Contributors
------------

* David Béal <david.beal@akretion.com>


Idea
----

Idea comes from module web_sheet_full_width (Luc De Meyer)

