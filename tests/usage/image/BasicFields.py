
from pyumldiagrams.BaseDiagram import BaseDiagram
from pyumldiagrams.Definitions import ClassDefinition
from pyumldiagrams.Definitions import DefinitionType
from pyumldiagrams.Definitions import FieldDefinition
from pyumldiagrams.Definitions import MethodDefinition
from pyumldiagrams.Definitions import Position
from pyumldiagrams.Definitions import Size
from pyumldiagrams.image.ImageDiagram import ImageDiagram


def buildFields() -> BaseDiagram.FieldsRepr:

    fields: BaseDiagram.FieldsRepr = []

    fieldFull:             FieldDefinition = FieldDefinition(name='FullField',             parameterType='int',   defaultValue='1')
    fieldTypeOnly:         FieldDefinition = FieldDefinition(name='FieldTypeOnly',         parameterType='float', defaultValue='')
    fieldDefaultValueOnly: FieldDefinition = FieldDefinition(name='FieldDefaultValueOnly', parameterType='',      defaultValue='23')

    fieldFull.visibility     = DefinitionType.Public
    fieldTypeOnly.visibility = DefinitionType.Private
    fieldDefaultValueOnly.visibility = DefinitionType.Protected

    fields.append(fieldFull)
    fields.append(fieldTypeOnly)
    fields.append(fieldDefaultValueOnly)

    return fields


fileName:        str             = 'BasicFields.png'
diagram:         ImageDiagram    = ImageDiagram(fileName=fileName)
fieldsTestClass: ClassDefinition = ClassDefinition(name='FieldsTestClass', position=Position(226, 102), size=Size(height=156, width=230))

fieldsTestClass.fields = buildFields()

initMethodDef: MethodDefinition = MethodDefinition(name='__init__', visibility=DefinitionType.Public)

fieldsTestClass.methods = [initMethodDef]

diagram.drawClass(classDefinition=fieldsTestClass)

diagram.write()
