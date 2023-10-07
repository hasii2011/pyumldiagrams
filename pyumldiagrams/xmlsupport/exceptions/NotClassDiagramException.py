
class NotClassDiagramException(Exception):

    def __init__(self, *args):
        super().__init__(args)

    def __str__(self):
        return f'Only class diagrams documents are supported'
