"""Return package-metadata readiness using the deployment protocol."""

import json
import sys
from importlib.metadata import version

if sys.argv[1:] != ["--deployment-check"]:
    raise SystemExit("This fixture only supports --deployment-check.")
print(json.dumps({"tool_id": "ceratops-deployment-fixture", "version": version("ceratops-deployment-fixture"), "ready": True}))
