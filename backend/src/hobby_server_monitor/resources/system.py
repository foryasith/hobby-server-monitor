"""Host system information and resource usage endpoint."""

from datetime import UTC, datetime
import os
import platform
import shutil
import socket

import falcon


def _read_memory() -> dict[str, int] | None:
    """Read Linux memory information from /proc/meminfo."""

    try:
        values: dict[str, int] = {}

        with open("/proc/meminfo", encoding="utf-8") as file:
            for line in file:
                key, value = line.split(":", maxsplit=1)
                values[key] = int(value.strip().split()[0]) * 1024

        total = values["MemTotal"]
        available = values["MemAvailable"]

        return {
            "total_bytes": total,
            "available_bytes": available,
            "used_bytes": max(total - available, 0),
        }
    except (OSError, KeyError, ValueError, IndexError):
        return None


def _read_uptime() -> float | None:
    """Read Linux host uptime in seconds."""

    try:
        with open("/proc/uptime", encoding="utf-8") as file:
            return round(float(file.read().split()[0]), 2)
    except (OSError, ValueError, IndexError):
        return None


class SystemResource:
    """Return a summary of host system resource usage."""

    def on_get(self, req: falcon.Request, resp: falcon.Response) -> None:
        """Handle GET /api/system requests."""

        disk = shutil.disk_usage("/")

        try:
            load_average = os.getloadavg()
        except OSError:
            load_average = None

        resp.status = falcon.HTTP_200
        resp.media = {
            "hostname": socket.gethostname(),
            "operating_system": platform.system(),
            "platform_release": platform.release(),
            "architecture": platform.machine(),
            "cpu_count": os.cpu_count(),
            "load_average": {
                "one_minute": load_average[0],
                "five_minutes": load_average[1],
                "fifteen_minutes": load_average[2],
            }
            if load_average
            else None,
            "memory": _read_memory(),
            "disk": {
                "total_bytes": disk.total,
                "used_bytes": disk.used,
                "free_bytes": disk.free,
            },
            "uptime_seconds": _read_uptime(),
            "collected_at": datetime.now(UTC).isoformat(),
        }