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

    def __init__(self, image=None, external_envs={}):
        if image:
            self.image = image
        self.add_external_env(external_envs)

    def add_external_env(self, envs):
        current = self.variables.copy()
        envs.update(current)
        self.variables.update(envs)

    def run(self):
        self.container = self.client.containers.run(
            self.image,
            detach=True,
            environment=self.variables,
        )

    def destroy(self):
        self.container.stop()
        self.container.remove(force=True, v=True)
