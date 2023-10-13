
from dataclasses import dataclass


class TestDefinitions:

    TEST_DPI: int = 72

    PDF_SUFFIX:            str = '.pdf'
    TEST_FILE_NAME_PREFIX: str = 'Test'


@dataclass
class Names:
    baseName:      str = ''
    generatedName: str = ''
