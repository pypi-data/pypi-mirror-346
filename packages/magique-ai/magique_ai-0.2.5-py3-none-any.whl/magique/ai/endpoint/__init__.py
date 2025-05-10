import sys
from pathlib import Path
import base64

from ..toolset import run_toolsets, ToolSet, tool
from ..tools.web_browse import WebBrowseToolSet
from ..tools.file_manager import FileManagerToolSet
from ..tools.python import PythonInterpreterToolSet
from ..constant import DEFAULT_SERVER_URL
from ..utils.remote import connect_remote
from ..tools.file_transfer import FileTransferToolSet


class Endpoint(FileTransferToolSet):
    def __init__(
        self,
        name: str = "pantheon-chatroom-endpoint",
        workspace_path: str = "./.pantheon-chatroom-workspace",
        worker_params: dict | None = None,
    ):
        Path(workspace_path).mkdir(parents=True, exist_ok=True)
        super().__init__(name, workspace_path, worker_params)
        self.services: list[ToolSet] = []
        self.outer_services: list[dict] = []
        self.create_services()

    @tool
    async def list_services(self) -> list[dict]:
        res = []
        for service in self.services:
            res.append({
                "name": service.worker.service_name,
                "id": service.worker.service_id,
            })
        for s in self.outer_services:
            res.append({
                "name": s["name"],
                "id": s["id"],
            })
        return res

    @tool
    async def fetch_image_base64(self, image_path: str) -> dict:
        """Fetch an image and return the base64 encoded image."""
        if '..' in image_path:
            return {"success": False, "error": "Image path cannot contain '..'"}
        i_path = self.path / image_path
        if not i_path.exists():
            return {"success": False, "error": "Image does not exist"}
        format = i_path.suffix.lower()
        if format not in [".jpg", ".jpeg", ".png", ".gif"]:
            return {"success": False, "error": "Image format must be jpg, jpeg, png or gif"}
        with open(i_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("utf-8")
            data_uri = f"data:image/{format};base64,{b64}"
        return {
            "success": True,
            "image_path": image_path,
            "data_uri": data_uri,
        }

    @tool
    async def add_service(self, service_id: str):
        """Add a service to the endpoint."""
        for s in self.services:
            if s.worker.service_id == service_id:
                return {"success": False, "error": "Service already exists"}
        try:
            s = await connect_remote(service_id, DEFAULT_SERVER_URL)
            info = await s.fetch_service_info()
            self.outer_services.append({
                "id": service_id,
                "name": info.service_name,
            })
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}

    @tool
    async def get_service(self, service_id_or_name: str) -> dict | None:
        """Get a service by id or name."""
        for s in self.services:
            if (
                s.worker.service_id == service_id_or_name
                or s.worker.service_name == service_id_or_name
            ):
                return {
                    "id": s.worker.service_id,
                    "name": s.worker.service_name,
                }
        for s in self.outer_services:
            if (
                s["id"] == service_id_or_name
                or s["name"] == service_id_or_name
            ):
                return s
        return None

    def create_services(self):
        toolset = PythonInterpreterToolSet(
            name="python_interpreter",
            workdir=str(self.path),
        )
        self.services.append(toolset)
        toolset = FileManagerToolSet(
            name="file_manager",
            path=str(self.path),
        )
        self.services.append(toolset)
        toolset = WebBrowseToolSet(
            name="web_browse",
        )
        self.services.append(toolset)

    async def run(self, log_level: str = "INFO"):
        from loguru import logger
        logger.remove()
        logger.add(sys.stderr, level=log_level)
        async with run_toolsets(self.services, log_level=log_level):
            logger.info(f"Remote Server: {self.worker.server_url}")
            logger.info(f"Service Name: {self.worker.service_name}")
            logger.info(f"Service ID: {self.worker.service_id}")
            return await self.worker.run()
