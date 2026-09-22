"""Health-check resource for service availability monitoring."""

from datetime import UTC, datetime

import falcon


class HealthResource:
    """Return the current availability state of the backend service."""

    def on_get(self, req: falcon.Request, resp: falcon.Response) -> None:
        """Handle GET /api/health requests."""

        resp.status = falcon.HTTP_200
        resp.media = {
            "status": "ok",
            "service": "hobby-server-monitor-api",
            "version": "0.1.0",
            "timestamp": datetime.now(UTC).isoformat(),
        }