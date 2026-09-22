"""Falcon application factory and WSGI entry point."""

import falcon

from hobby_server_monitor.resources.health import HealthResource


def create_app() -> falcon.App:
    """Create and configure the Hobby Server Monitor API."""

    application = falcon.App()

    health_resource = HealthResource()
    application.add_route("/api/health", health_resource)

    return application


app = create_app()