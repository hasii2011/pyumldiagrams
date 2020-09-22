from typing import final

from pyumldiagrams.BaseDiagram import BaseDiagram
from pyumldiagrams.Definitions import ClassDefinition
from pyumldiagrams.Definitions import DefinitionType
from pyumldiagrams.Definitions import FieldDefinition
from pyumldiagrams.Definitions import LinePositions
from pyumldiagrams.Definitions import LineType
from pyumldiagrams.Definitions import MethodDefinition
from pyumldiagrams.Definitions import ParameterDefinition
from pyumldiagrams.Definitions import Position
from pyumldiagrams.Definitions import Size
from pyumldiagrams.Definitions import UmlLineDefinition
from pyumldiagrams.Definitions import UmlLineDefinitions

from tests.TestBase import TestBase


class TestDiagramParent(TestBase):

    UNIT_TEST_HEADER:               final = 'Unit Test Header'
    UNIT_TEST_SOPHISTICATED_HEADER: final = 'Pyut Export Version 6.0'

    BASE_TEST_CLASS_NAME: str = 'TestClassName'

    def _buildCar(self) -> ClassDefinition:

        car: ClassDefinition = ClassDefinition(name='Car', position=Position(107, 30), size=Size(width=266, height=100))

        initMethodDef:      MethodDefinition = self._buildInitMethod()
        descMethodDef:      MethodDefinition = MethodDefinition(name='getDescriptiveName', visibility=DefinitionType.Public)
        odometerMethodDef:  MethodDefinition = MethodDefinition(name='readOdometer',       visibility=DefinitionType.Public)
        updateOdoMethodDef: MethodDefinition = MethodDefinition(name='updateOdometer',     visibility=DefinitionType.Public)
        incrementMethodDef: MethodDefinition = MethodDefinition(name='incrementOdometer',  visibility=DefinitionType.Protected)

        mileageParam: ParameterDefinition = ParameterDefinition(name='mileage', defaultValue='1')
        updateOdoMethodDef.parameters = [mileageParam]

        milesParam: ParameterDefinition = ParameterDefinition(name='miles', parameterType='int')
        incrementMethodDef.parameters = [milesParam]

        car.methods = [initMethodDef, descMethodDef, odometerMethodDef, updateOdoMethodDef, incrementMethodDef]

        return car

    def _buildInitMethod(self) -> MethodDefinition:

        initMethodDef:  MethodDefinition    = MethodDefinition(name='__init__', visibility=DefinitionType.Public)

        initParam:  ParameterDefinition = ParameterDefinition(name='make',  parameterType='str', defaultValue='')
        modelParam: ParameterDefinition = ParameterDefinition(name='model', parameterType='str', defaultValue='')
        yearParam:  ParameterDefinition = ParameterDefinition(name='year',  parameterType='int', defaultValue='1957')

        initMethodDef.parameters = [initParam, modelParam, yearParam]

        return initMethodDef

    def _buildCat(self) -> ClassDefinition:

        cat: ClassDefinition = ClassDefinition(name='gato', position=Position(536, 19), size=Size(height=74, width=113))

        initMethod:     MethodDefinition = MethodDefinition('__init')
        sitMethod:      MethodDefinition = MethodDefinition('sit')
        rollOverMethod: MethodDefinition = MethodDefinition('rollOver')

        cat.methods = [initMethod, sitMethod, rollOverMethod]

        return cat

    def _buildOpie(self) -> ClassDefinition:

        opie: ClassDefinition = ClassDefinition(name='Opie', position=Position(495, 208), size=Size(width=216, height=87))

        publicMethod: MethodDefinition = MethodDefinition(name='publicMethod', visibility=DefinitionType.Public, returnType='bool')
        paramDef: ParameterDefinition  = ParameterDefinition(name='param', parameterType='float', defaultValue='23.0')

        publicMethod.parameters = [paramDef]

        opie.methods = [publicMethod]

        return opie

    def _buildElectricCar(self) -> ClassDefinition:

        electricCar: ClassDefinition = ClassDefinition(name='ElectricCar', position=Position(52, 224), size=Size(width=173, height=64))

        initMethod: MethodDefinition = MethodDefinition(name='__init__')
        descMethod: MethodDefinition = MethodDefinition(name='describeBattery')

        makeParameter:  ParameterDefinition = ParameterDefinition(name='make')
        modelParameter: ParameterDefinition = ParameterDefinition(name='model')
        yearParameter:  ParameterDefinition = ParameterDefinition(name='year')

        initMethod.parameters = [makeParameter, modelParameter, yearParameter]
        electricCar.methods = [initMethod, descMethod]
        return electricCar

    def _buildNameTestCase(self) -> ClassDefinition:

        namesTest: ClassDefinition = ClassDefinition(name='NamesTestCase', position=Position(409, 362), size=Size(height=65, width=184))

        testFirst:    MethodDefinition = MethodDefinition(name='testFirstLasName')
        formattedName: MethodDefinition = MethodDefinition(name='getFormattedName')

        firstParam:  ParameterDefinition = ParameterDefinition(name='first')
        lastParam:  ParameterDefinition = ParameterDefinition(name='last')

        formattedName.parameters = [firstParam, lastParam]
        namesTest.methods = [testFirst, formattedName]

        return namesTest

    def _buildSophisticatedLineDefinitions(self) -> UmlLineDefinitions:

        startPosition: Position = Position(600, 208)
        endPosition:   Position = Position(600, 93)
        opieToCatLinePositions: LinePositions = [startPosition, endPosition]

        opieToCat: UmlLineDefinition = UmlLineDefinition(lineType=LineType.Inheritance, linePositions=opieToCatLinePositions)

        startPosition2: Position = Position(190, 224)
        endPosition2:   Position = Position(190, 130)

        eCarToCarLinePositions: LinePositions = [startPosition2, endPosition2]
        eCarToCar: UmlLineDefinition = UmlLineDefinition(lineType=LineType.Inheritance, linePositions=eCarToCarLinePositions)
        lineDefinitions: UmlLineDefinitions = [
            opieToCat, eCarToCar
        ]

        return lineDefinitions

    def _buildTopClass(self) -> ClassDefinition:
        top: ClassDefinition = ClassDefinition(name='TopClass', position=Position(409.0, 159.0), size=Size(height=100, width=113))
        return top

    def _buildLeftClass(self) -> ClassDefinition:
        left: ClassDefinition = ClassDefinition(name='LeftClass', position=Position(266.0, 359.0), size=Size(height=99.0, width=127.0))
        return left

    def _buildRightClass(self) -> ClassDefinition:
        right: ClassDefinition = ClassDefinition(name='RightClass', position=Position(522.0, 354.0), size=Size(height=107.0, width=167.0))
        return right

    def _buildBendTest(self):

        startPos: Position = Position(x=330.0, y=359.0)
        cp1Pos:   Position = Position(x=330.0, y=286.0)
        cp2Pos:   Position = Position(x=178.0, y=286.0)
        cp3Pos:   Position = Position(x=178.0, y=207.0)
        endPos:   Position = Position(x=409.0, y=207.0)

        bigBends: LinePositions = [startPos, cp1Pos, cp2Pos, cp3Pos, endPos]

        leftToTop: UmlLineDefinition = UmlLineDefinition(lineType=LineType.Inheritance, linePositions=bigBends)

        bentLineDefinitions: UmlLineDefinitions = [leftToTop]

        return bentLineDefinitions

    def _buildFields(self) -> BaseDiagram.FieldsRepr:

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
