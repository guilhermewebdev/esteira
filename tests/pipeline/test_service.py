from esteira.pipeline.service import Service

def test_instance():
    envs = {
        "POSTGRES_DB": "nice_marmot",
        "POSTGRES_USER": "runner",
        "POSTGRES_PASSWORD": "pass",
        "POSTGRES_HOST_AUTH_METHOD": "trust",
    }
    service = Service(
        'postgres',
        external_envs=envs
    )
    service.run()
    service.container.exec_run('ls /')
    service.destroy()