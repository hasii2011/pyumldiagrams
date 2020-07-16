

class DiagramCommon:
    """
    All the defaults defined here are expressed in points
    """
    LEFT_MARGIN: int = 8
    TOP_MARGIN:  int = 8

    DEFAULT_HORIZONTAL_GAP: int = 60
    DEFAULT_VERTICAL_GAP:   int = 60

    @classmethod
    def toPdfPoints(cls, pixelNumber: float, dpi: int) -> int:
        """

        points = pixels * 72 / DPI

        Args:
            pixelNumber:  From the display
            dpi:  dots per inch of source display

        Returns:  A pdf point value to use to position on a generated document

        """
        points: int = int((pixelNumber * 72)) // dpi

        return points
