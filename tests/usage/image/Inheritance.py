
from pyumldiagrams.Definitions import ClassDefinition
from pyumldiagrams.Definitions import LinePositions
from pyumldiagrams.Definitions import LineType
from pyumldiagrams.Definitions import Position
from pyumldiagrams.Definitions import Size
from pyumldiagrams.Definitions import UmlLineDefinition

from pyumldiagrams.image.ImageDiagram import ImageDiagram

diagram:  ImageDiagram    = ImageDiagram(fileName='Inheritance.png')

cat:  ClassDefinition = ClassDefinition(name='Gato', position=Position(536, 19), size=Size(height=74, width=113))
opie: ClassDefinition = ClassDefinition(name='Opie', position=Position(495, 208), size=Size(width=216, height=87))

diagram.drawClass(classDefinition=cat)
diagram.drawClass(classDefinition=opie)

linePositions: LinePositions     = LinePositions([Position(600, 208), Position(600, 93)])
opieToCat:     UmlLineDefinition = UmlLineDefinition(lineType=LineType.Inheritance, linePositions=linePositions)

diagram.drawUmlLine(lineDefinition=opieToCat)
diagram.write()
