"""Falcon application factory and WSGI entry point."""

import falcon

from hobby_server_monitor.resources.health import HealthResource
from hobby_server_monitor.resources.system import SystemResource


def create_app() -> falcon.App:
    """Create and configure the Hobby Server Monitor API."""

    application = falcon.App()

    application.add_route("/api/health", HealthResource())
    application.add_route("/api/system", SystemResource())

    return application


app = create_app()