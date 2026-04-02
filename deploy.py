import logging
from truefoundry.deploy import (
    Pip,
    PythonBuild,
    LocalSource,
    Resources,
    Port,
    Build,
    NodeSelector,
    Service,
)

logging.basicConfig(level=logging.INFO)

service = Service(
    name="sample-service",
    image=Build(
        build_source=LocalSource(local_build=False),
        build_spec=PythonBuild(
            python_version="3.11",
            build_context_path="./",
            python_dependencies=Pip(),
            command="gunicorn -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 server:app",
        ),
    ),
    resources=Resources(
        cpu_request=0.5,
        cpu_limit=0.5,
        memory_request=1000,
        memory_limit=1000,
        ephemeral_storage_request=500,
        ephemeral_storage_limit=500,
        node=NodeSelector(capacity_type="spot_fallback_on_demand"),
    ),
    env={"MODEL_DIR": "."},
    ports=[
        Port(
            port=8000,
            protocol="TCP",
            expose=True,
            app_protocol="http",
            host="tfy-test-usw2-ee.my.automationanywhere.digital",
            path="/sample-service-context-intelligence-dev-ws-8000/",
        )
    ],
    workspace_fqn="tfy-aws-test-usw2-ee:context-intelligence-dev-ws",
    replicas=1.0,
)


service.deploy(
    workspace_fqn="tfy-aws-test-usw2-ee:context-intelligence-dev-ws", wait=False
)
