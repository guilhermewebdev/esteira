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

    def run(self):
        self.container = self.client.containers.run(
            self.image,
            detach=True,
            stdin_open=True,
            environment=self.variables,
            hostname=str(self.host)
        )
        self.container.start()
