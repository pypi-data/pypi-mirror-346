import functools
import importlib
import logging
import asyncio
import os
import sys

import click
from dbus_fast.aio import MessageBus
from dbus_fast.service import ServiceInterface, dbus_property
from dbus_fast.constants import BusType, PropertyAccess
from dbus_fast.service import signal

from openhydroponics.base.endpoint import Endpoint
from openhydroponics.net import Node, NodeManager
from openhydroponics.service.endpoint import wrap_endpoint


class NodeInterface(ServiceInterface):
    def __init__(self, bus: MessageBus, node: Node):
        super().__init__("com.openhydroponics.NodeInterface")
        self._bus = bus
        self._node = node
        self._endpoints = []
        for endpoint in node:
            endpoint_interface = EndpointInterface(self, endpoint)
            self._endpoints.append(endpoint_interface)
            self._bus.export(endpoint_interface.object_path, endpoint_interface)
            self._bus.export(
                endpoint_interface.object_path, endpoint_interface.wrapped_endpoint
            )

    @dbus_property(access=PropertyAccess.READ)
    def Interviewed(self) -> "b":
        return self._node.interviewed

    @property
    def object_path(self):
        return f"/com/openhydroponics/nodes/{str(self._node.uuid).replace('-', '_')}"

    @dbus_property(access=PropertyAccess.READ)
    def UUID(self) -> "s":
        return str(self._node.uuid)


class EndpointInterface(ServiceInterface):
    def __init__(self, node: NodeInterface, endpoint: Endpoint):
        super().__init__("com.openhydroponics.EndpointMetaDataInterface")
        self._node = node
        self._endpoint = endpoint
        self._wrapped_endoint = wrap_endpoint(endpoint)

    @property
    def wrapped_endpoint(self):
        return self._wrapped_endoint

    @dbus_property(access=PropertyAccess.READ)
    def EndpointClass(self) -> "u":
        return self._endpoint.ENDPOINT_CLASS

    @dbus_property(access=PropertyAccess.READ)
    def EndpointId(self) -> "u":
        return self._endpoint.endpoint_id

    @dbus_property(access=PropertyAccess.READ)
    def EndpointInterface(self) -> "s":
        return self._wrapped_endoint.DBUS_INTERFACE

    @property
    def object_path(self):
        return f"{self._node.object_path}/{self._endpoint.endpoint_id}"


class NodeManagerInterface(ServiceInterface):
    def __init__(self, bus):
        super().__init__("com.openhydroponics.NodeManager")
        self._bus: MessageBus = bus
        self._nm: NodeManager = NodeManager()
        self._nm.on_node_added.connect(self._on_node_added)
        self._nodes = []

    @signal()
    def NodeAdded(self, object_path: str) -> "o":
        return object_path

    async def init(self):
        await self._nm.init()

    def _on_node_added(self, node: Node):
        if not node.interviewed:
            # Re call ourselves when the interview is done
            node.on_interview_done.connect(
                functools.partial(self._on_node_added, node=node)
            )
            return
        node_interface = NodeInterface(self._bus, node)
        self._nodes.append(node_interface)
        self._bus.export(node_interface.object_path, node_interface)
        self.NodeAdded(node_interface.object_path)


async def main(bus_type: str):
    if bus_type == "system":
        bus = BusType.SYSTEM
    else:
        bus = BusType.SESSION

    logging.basicConfig(
        format="%(asctime)s %(name)-20s %(levelname)-7s: %(message)s",
        level=logging.DEBUG,
        datefmt="%H:%M:%S",
    )
    bus = await MessageBus(bus_type=bus).connect()

    interface = NodeManagerInterface(bus)
    await interface.init()

    bus.export("/com/openhydroponics/nodes", interface)
    await bus.request_name("com.openhydroponics")

    try:
        await bus.wait_for_disconnect()
    except Exception:
        # Ignore all exceptions, we are just waiting for the bus to disconnect
        _LOG.error("Exception while waiting for bus to disconnect", exc_info=True)


@click.group(invoke_without_command=True)
@click.pass_context
@click.option(
    "--bus",
    type=click.Choice(["system", "session"], case_sensitive=False),
    default="system",
    help="Select the dbus bus to connect to.",
)
def daemon(ctx, bus):
    if ctx.invoked_subcommand is not None:
        return
    try:
        asyncio.run(main(bus))
    except KeyboardInterrupt:
        print("Exiting...")


@daemon.command()
@click.option(
    "--user",
    is_eager=True,
    default=os.getenv("SUDO_USER", os.getenv("USER")),
    help="User to run the service as.",
)
def install(user):
    """Install the service"""
    click.echo("Installing the OpenHydroponics Service...")
    if os.geteuid() != 0:
        click.echo("Please run this command as root.")
        return
    params = {
        "user": user,
        "path": os.path.abspath(sys.argv[0]),
    }
    resource_path = importlib.resources.files("openhydroponics").joinpath(
        "conf", "systemd", "openhydroponicsd.service"
    )
    with open(resource_path, "r") as f:
        service_file = f.read().format_map(params)
    with open("/etc/systemd/system/openhydroponicsd.service", "w") as f:
        f.write(service_file)

    resource_path = importlib.resources.files("openhydroponics").joinpath(
        "conf", "dbus", "com.openhydroponics.conf"
    )
    with open(resource_path, "r") as f:
        dbus_file = f.read().format_map(params)
    with open("/etc/dbus-1/system.d/com.openhydroponics.conf", "w") as f:
        f.write(dbus_file)

    os.system("systemctl enable openhydroponicsd")
    os.system("systemctl daemon-reload")  # To enable the d-bus rules
    os.system("systemctl start openhydroponicsd")
    click.echo("Service installed.")


if __name__ == "__main__":
    daemon()
