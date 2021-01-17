import docker
from functools import reduce
from docker.api.client import APIClient

class Task:
    image = 'ubuntu'
    container = None
    client = docker.from_env()
    variables = {}
    api_client = APIClient(base_url='unix://var/run/docker.sock')

    @property
    def env_as_list(self):
        return list(reduce(
            lambda index, value: f'{index}={value}',
            self.variables.items(),
            ''
        ))

    def __init__(self, external_envs={}, image=None):
        if image:
            self.image = image
        self.add_external_env(external_envs)

    def add_external_env(self, envs):
        current = self.variables.copy()
        envs.update(current)
        self.variables.update(envs)

    def destroy(self):
        self.container.stop()
        self.container.remove()