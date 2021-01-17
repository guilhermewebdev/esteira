from esteira.pipeline.stage import Stage
from pathlib import Path

BASE_DIR = Path(__file__).parent.absolute()


def test_instance():
    class TestShell(Stage):
        script = [
            'echo "hello world"'
        ]
    test = TestShell(BASE_DIR)
    test.run()