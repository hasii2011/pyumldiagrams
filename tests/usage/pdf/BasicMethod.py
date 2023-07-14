
from pyumldiagrams.Definitions import ClassDefinition
from pyumldiagrams.Definitions import DefinitionType
from pyumldiagrams.Definitions import MethodDefinition
from pyumldiagrams.Definitions import ParameterDefinition
from pyumldiagrams.Definitions import Position
from pyumldiagrams.Definitions import Size

from pyumldiagrams.pdf.PdfDiagram import PdfDiagram


diagram:  PdfDiagram       = PdfDiagram(fileName=f'BasicMethod.pdf', dpi=75)
position: Position         = Position(107, 30)
size:     Size             = Size(width=266, height=100)
car:       ClassDefinition = ClassDefinition(name='Car', position=position, size=size)

initMethodDef: MethodDefinition   = MethodDefinition(name='__init__', visibility=DefinitionType.Public)
initParam:    ParameterDefinition = ParameterDefinition(name='make', parameterType='str', defaultValue='')

initMethodDef.parameters = [initParam]
car.methods = [initMethodDef]

diagram.drawClass(car)

diagram.write()
