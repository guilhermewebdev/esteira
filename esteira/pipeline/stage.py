from .task import Task


class Stage(Task):
    before_script = []
    script = []
    repo_dir = ''

    def __init__(self, repo_dir, image=None, external_envs={}):
        self.repo_dir = repo_dir
        super().__init__(external_envs=external_envs, image=image)

    def each_script(self, scripts):
        image = self.client.images.get(self.image)
        for script in scripts:
            print(f'> {script}')
            self.container = self.client.containers.run(
                image,
                command=script,
                stderr=True,
                stdin_open=False,
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
        self.each_script(self.before_script)
        self.each_script(self.script)
        self.destroy()


