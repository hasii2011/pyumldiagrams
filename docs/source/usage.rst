Usage
=====

.. _installation:

Installation
------------

To use pyumldiagrams, first install it using pip:

.. code-block:: console

   (.venv) $ pip install pyumldiagrams

.. code-block:: console

=================================
Create a basic pdf class diagram
=================================

.. code-block:: console

    from pyumldiagrams.pdf.PdfDiagram import PdfDiagram
    from pyumldiagrams.xmlsupport.ToClassDefinition import ToClassDefinition


    diagram:  PdfDiagram      = PdfDiagram(fileName='basicClass.pdf', dpi=75)
    classDef: ClassDefinition = ClassDefinition(name='BasicClass', size=Size(width=100, height=100))

    diagram.drawClass(classDef)
    diagram.write()

Produces the following output

.. image:: images/Test-Basic.png

