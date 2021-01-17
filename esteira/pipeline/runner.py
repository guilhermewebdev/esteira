import os
from git import Repo
from pathlib import Path

class Runner:
    stages = []
    stage_classes = []
    services = []
    variables = {}
    repo = None

    def __init__(self, stage_classes, stages,  repo_dir=None, services=[], variables={}):
        self.repo = Repo(str(repo_dir if repo_dir else Path(__file__).parent.absolute()))
        self.stages = stages
        self.stage_classes = stage_classes
        self.services = services
        sys_envs = os.environ.copy()
        sys_envs.update(variables)
        self.variables = sys_envs

    def setup_services(self):
        print('Starting services')
        for service in self.services:
            service.run()
        print('Done starting services')

    def stop_services(self):
        print('Stoping services')
        for service in self.services:
            print(f'Stoping {service.__class__.__name__}')
            service.destroy()
        print('Services stopped')

    def filter_branch(self, stg_class):
        if hasattr(stg_class, 'only'):
            return self.repo.active_branch.name in stg_class.only
        return True

    def filter_stages(self, stage):
        filter_stage = lambda stg_class: stg_class.stage == stage
        by_stage = list(filter(
            filter_stage,
            self.stage_classes
        ))
        return list(filter(
            self.filter_branch,
            by_stage,
        ))

    def run_stage(self, stage):
        print(f'Running stages {stage}s')
        to_run = self.filter_stages(stage)
        for stg_class in to_run:
            print(f'Running {stg_class.__name__}')
            script = stg_class(self.variables)
            script.run()

    def run_stages(self):
        print('Runnig stages')
        for stage in self.stages:
            self.run_stage(stage)
        print('Done running stages')

    def __call__(self):
        print('Starting..')
        try:
            self.setup_services()
            self.run_stages()
        except Exception as error:
            print(error)
        finally:
            self.stop_services()
    

