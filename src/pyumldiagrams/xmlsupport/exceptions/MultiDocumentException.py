
class MultiDocumentException(Exception):

    def __init__(self, *args):
        super().__init__(args)

    def __str__(self):
        return f'Only single document projects are supported'
