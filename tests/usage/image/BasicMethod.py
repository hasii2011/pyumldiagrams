
from pyumldiagrams.Definitions import ClassDefinition
from pyumldiagrams.Definitions import VisibilityType
from pyumldiagrams.Definitions import MethodDefinition
from pyumldiagrams.Definitions import Methods
from pyumldiagrams.Definitions import ParameterDefinition
from pyumldiagrams.Definitions import Parameters
from pyumldiagrams.Definitions import Position
from pyumldiagrams.Definitions import Size

from pyumldiagrams.image.ImageDiagram import ImageDiagram

diagram:  ImageDiagram    = ImageDiagram(fileName='BasicMethod.png')

position: Position         = Position(107, 30)
size:     Size             = Size(width=266, height=100)
car:       ClassDefinition = ClassDefinition(name='Car', position=position, size=size)

initMethodDef: MethodDefinition   = MethodDefinition(name='__init__', visibility=VisibilityType.Public)
initParam:    ParameterDefinition = ParameterDefinition(name='make', parameterType='str', defaultValue='')

initMethodDef.parameters = Parameters([initParam])
car.methods              = Methods([initMethodDef])

diagram.drawClass(car)

diagram.write()
