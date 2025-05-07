from uuid import UUID

from dbus_fast.aio import MessageBus
from dbus_fast.constants import BusType

from openhydroponics.base import NodeManagerBase
from openhydroponics.dbus import Node

BUS_NAME = "com.openhydroponics"


class NodeManager(NodeManagerBase):
    __slots__ = (
        "_bus",
        "_bus_type",
        "_dbus_interface",
        "_interface",
        "_initialized",
    )

    def __init__(self, bus_type: BusType = BusType.SYSTEM):
        super().__init__()
        self._bus = None
        self._bus_type: BusType = bus_type
        self._initialized = False
        self._interface = None
        self._dbus_interface = None

    async def init(self):
        if self._initialized:
            return

        if not self._bus:
            self._bus = await MessageBus(bus_type=self._bus_type).connect()

        if not self._dbus_interface:
            introspection = await self._bus.introspect(
                "org.freedesktop.DBus", "/org/freedesktop/DBus"
            )
            proxy = self._bus.get_proxy_object(
                "org.freedesktop.DBus", "/org/freedesktop/DBus", introspection
            )
            self._dbus_interface = proxy.get_interface("org.freedesktop.DBus")
            self._dbus_interface.on_name_owner_changed(self._name_owner_changed)

        if not self._interface:
            has_owner = await self._dbus_interface.call_name_has_owner(BUS_NAME)
            if not has_owner:
                # Service is not running
                return

            introspection = await self._bus.introspect(
                BUS_NAME, "/com/openhydroponics/nodes"
            )

            proxy = self._bus.get_proxy_object(
                BUS_NAME, "/com/openhydroponics/nodes", introspection
            )

            self._interface = proxy.get_interface("com.openhydroponics.NodeManager")
            self._interface.on_node_added(self._add_node_from_path)

            for child in introspection.nodes:
                path = f"{introspection.name}/{child.name}"
                await self._add_node_from_path(path)
        self._initialized = True

    async def _add_node_from_path(self, object_path: str):
        introspection = await self._bus.introspect(BUS_NAME, object_path)
        proxy_object = self._bus.get_proxy_object(BUS_NAME, object_path, introspection)

        interface = proxy_object.get_interface("com.openhydroponics.NodeInterface")
        uuid = UUID(await interface.get_uuid())
        if self.get_node(uuid):
            # Node already exists
            return
        node = Node(uuid, proxy_object)
        await node.init(self._bus, introspection)
        self.add_node(uuid, node)

    async def _name_owner_changed(self, name: str, old_owner: str, new_owner: str):
        if name != BUS_NAME:
            return
        if old_owner == "" and new_owner != "":
            # Service started
            if not self._initialized:
                await self.init()
