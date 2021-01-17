from esteira.pipeline import Runner, Stage
from pathlib import Path


def test_instance():
    stages = [
        'test'
    ]
    class Test(Stage):
        script = [
            'echo "hello world'
        ]
    runner = Runner(
        stage_classes=[Test],
        stages=stages,
        repo_dir=Path(__file__).parent.parent.parent.absolute()
    )
    runner()