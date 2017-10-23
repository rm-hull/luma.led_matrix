API Documentation
-----------------
.. automodule:: luma.led_matrix
    :members:
    :undoc-members:
    :show-inheritance:

.. inheritance-diagram:: luma.core.device luma.core.mixin luma.core.virtual luma.led_matrix.device

Upgrading
"""""""""
.. warning::
   Version 0.3.0 was released on 19 January 2017: this came with a rename of the
   project in github from **max7219** to **luma.led_matrix** to reflect the changing
   nature of the codebase. It introduces a complete rewrite of the codebase to bring
   it in line with other 'luma' implementations.

   There is no direct migration path, but the old `documentation <https://max7219.readthedocs.io>`_
   and `PyPi packages <https://pypi.python.org/pypi/max7219>`_ will remain
   available indefinitely, but that deprecated codebase will no longer recieve 
   updates or fixes.
   
   This breaking change was necessary to be able to add different classes of
   devices, so that they could reuse core components.

:mod:`luma.led_matrix.device`
"""""""""""""""""""""""""""""
.. automodule:: luma.led_matrix.device
    :members:
    :inherited-members:
    :undoc-members:
    :show-inheritance:
