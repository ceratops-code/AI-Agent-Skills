"""Small JSON-RPC wire probe for interoperability with an actual stdio server.

This is test code, not a replacement MCP runtime. The reader is bounded and
every child is closed by the context owner, including failed assertions.
"""

import json
import queue
import subprocess
import threading
from typing import Any, TextIO, cast


class WireClient:
    def __init__(self, command, *, env=None):
        self.process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE, text=True, encoding="utf-8", env=env,
                                        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
        self.input = cast(TextIO, self.process.stdin)
        self.output = cast(TextIO, self.process.stdout)
        self.error_output = cast(TextIO, self.process.stderr)
        self.responses: queue.Queue[dict[str, Any]] = queue.Queue()
        self.errors: list[str] = []
        self.sequence = 0

        def read():
            for line in self.output:
                self.responses.put(json.loads(line))
            self.responses.put({"closed": True})

        def errors():
            for line in self.error_output:
                self.errors.append(line)

        threading.Thread(target=read, daemon=True).start()
        threading.Thread(target=errors, daemon=True).start()

    def request(self, method, params=None):
        self.sequence += 1
        self.input.write(json.dumps({"jsonrpc": "2.0", "id": self.sequence, "method": method, "params": params or {}}) + "\n")
        self.input.flush()
        while True:
            message = self.responses.get(timeout=45)
            if message.get("closed"):
                raise AssertionError("MCP server exited: " + "".join(self.errors)[-2000:])
            if message.get("id") == self.sequence:
                return message

    def __enter__(self):
        try:
            initialized = self.request("initialize", {"protocolVersion": "2025-03-26", "capabilities": {}, "clientInfo": {"name": "deployment-test", "version": "1.0.0"}})
            assert "result" in initialized, initialized
            self.input.write('{"jsonrpc":"2.0","method":"notifications/initialized"}\n')
            self.input.flush()
            return self
        except BaseException:
            self.__exit__()
            raise

    def __exit__(self, *exc):
        self.input.close()
        try:
            self.process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            self.process.terminate()
            self.process.wait(timeout=5)
        self.output.close()
        self.error_output.close()
