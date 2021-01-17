from .task import Task

class Service(Task):
    service = None
    host = ''

    def __init__(self, image_name, host=None, external_envs={}):
        if host:
            self.host = host
        else:
            self.host = image_name.split(':')[0]
        super().__init__(external_envs=external_envs, image=image_name)

    def run(self, variables={}):
        variables.update(self.variables)
        self.container = self.client.containers.run(
            self.image,
            detach=True,
            environment=variables,
            hostname=str(self.host)
        )
