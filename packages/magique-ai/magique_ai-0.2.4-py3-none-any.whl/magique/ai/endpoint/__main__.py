import os

import fire

from . import Endpoint


async def main(
        service_name: str = "pantheon-chatroom-endpoint",
        workspace_path: str = "./.pantheon-chatroom-workspace",
        **worker_params
        ):
    if not os.path.exists(workspace_path):
        os.makedirs(workspace_path)
    endpoint = Endpoint(
        service_name,
        workspace_path,
        **worker_params
    )
    await endpoint.run()


if __name__ == "__main__":
    fire.Fire(main)
