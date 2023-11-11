
from typing import Tuple

from dataclasses import dataclass

from pyumldiagrams.Definitions import Position
from pyumldiagrams.Definitions import AttachmentSide


@dataclass(eq=True)
class AbsolutePosition:
    """
    """
    x: int = 0
    y: int = 0


class CommonAbsolute:
    """
    This class of computations resides here instead of common because it uses the Position
    class from Definitions and not and InternalPosition class which is relative to the
    particular output type (pdf/image)
    """
    X_FUDGE_FACTOR: int = 9
    Y_FUDGE_FACTOR: int = 9

    @classmethod
    def computeAbsoluteLabelPosition(cls, srcPosition: Position, dstPosition: Position, labelPosition: Position) -> Tuple[int, int]:
        """
        Label  positions are relative to the line they are attached to;

        Args:
            srcPosition:
            dstPosition:
            labelPosition:
        """
        xLength: int = abs(srcPosition.x - dstPosition.x)
        yLength: int = abs(srcPosition.y - dstPosition.y)

        if srcPosition.x < dstPosition.x:
            x: int = srcPosition.x + (xLength // 2) + labelPosition.x
            if cls.doXAdjustment(srcPosition=srcPosition, dstPosition=dstPosition) is True:
                x += CommonAbsolute.X_FUDGE_FACTOR
        else:
            x = dstPosition.x + (xLength // 2) + labelPosition.x
            if cls.doXAdjustment(srcPosition=srcPosition, dstPosition=dstPosition) is True:
                x -= CommonAbsolute.X_FUDGE_FACTOR

        if srcPosition.y < dstPosition.y:
            y: int = srcPosition.y + (yLength // 2) + labelPosition.y
        else:
            y = dstPosition.y + (yLength // 2) + labelPosition.y

        y += CommonAbsolute.Y_FUDGE_FACTOR

        return x, y

    @classmethod
    def doXAdjustment(cls, srcPosition: Position, dstPosition: Position) -> bool:

        ans: bool = True

        placement: AttachmentSide = cls.attachmentSide(srcX=srcPosition.x, srcY=srcPosition.y, dstX=dstPosition.x, dstY=dstPosition.y)

        if placement == AttachmentSide.NORTH or placement == AttachmentSide.SOUTH:
            ans = False

        return ans

    @classmethod
    def attachmentSide(cls, srcX: int, srcY: int, dstX: int, dstY: int) -> AttachmentSide:
        """
        Given a source and destination, returns where the destination
        is located according to the source.

        Args:
            srcX:   X pos of src point
            srcY:   Y pos of src point
            dstX:  X pos of dest point
            dstY:  Y pos of dest point

        Returns:  The attachment side
        """
        deltaX = srcX - dstX
        deltaY = srcY - dstY
        if deltaX > 0:  # dest is not east
            if deltaX > abs(deltaY):  # dest is west
                return AttachmentSide.WEST
            elif deltaY > 0:
                return AttachmentSide.NORTH
            else:
                return AttachmentSide.SOUTH
        else:  # dest is not west
            if -deltaX > abs(deltaY):  # dest is east
                return AttachmentSide.EAST
            elif deltaY > 0:
                return AttachmentSide.NORTH
            else:
                return AttachmentSide.SOUTH
