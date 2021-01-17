from esteira.pipeline.task import Task

def test_instance():
    task = Task()
    assert task.image == 'ubuntu'
    task.run()
    response = task.container.wait()
    print(task.container.logs())
    assert response.get('StatusCode') == 0, task.container.logs()
    assert response.get('Error') == None
    task.destroy()
    assert task.container.status != 'running'