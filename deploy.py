import logging
from truefoundry.deploy import (
    Build,
    Resources,
    PythonBuild,
    LocalSource,
    NodeSelector,
    Service,
    Port,
)

logging.basicConfig(level=logging.INFO)

service = Service(
    name="fisher-iris-dataset-example",
    image=Build(
        build_source=LocalSource(),
        build_spec=PythonBuild(
            build_context_path="./",
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
    env={"KEY": "VALUE"},
    ports=[
        Port(
            port=8000,
            protocol="TCP",
            expose=True,
            app_protocol="http",
            host="tfy-test-usw2-ee.my.automationanywhere.digital",
            path="/fisher-iris-dataset-example-context-intelligence-dev-ws-8000/",
        )
    ],
    replicas=1.0,
)


service.deploy(
    workspace_fqn="tfy-aws-test-usw2-ee:context-intelligence-dev-ws", wait=False
)
