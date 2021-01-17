from .task import Task


class Stage(Task):
    before_script = []
    script = []
    repo_dir = ''

    def __init__(self, image, repo_dir, external_envs={}):
        super().__init__(external_envs=external_envs, image=image)

    def run_script(self):
        script_list = self.before_script + self.script
        image = self.client.images.get(self.image)
        for script in script_list:
            print(f'> {script}')
            self.container = self.client.containers.run(
                image,
                command=script,
                stdin_open=False,
                stderr=True,
                working_dir='/builds',
                volumes={
                    self.repo_dir: {
                        'bind': '/builds',
                        'mode': 'rw'
                    }
                },
                environment=self.variables,
                detach=True,
                hostname=f'{self.__class__.__name__}'.lower()
            )
            for log in self.container.logs(stream=True, stderr=True, follow=True):
                print(log.decode('utf-8'))
            response = self.container.wait()
            assert response.get('StatusCode') == 0, 'Code returned ' + str(response.get('StatusCode'))
            assert response.get('Error') == None, str(response.get('Error'))
            image = self.container.commit(f'{self.__class__.__name__}'.lower())

    def run(self):
        self.run_script()
        self.destroy()


