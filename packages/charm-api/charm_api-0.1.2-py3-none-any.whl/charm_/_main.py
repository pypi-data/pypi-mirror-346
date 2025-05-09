import collections.abc
import json
import logging
import os
import subprocess
import types
import typing

# Use package name instead of module name
logger = logging.getLogger(__name__.rsplit(".", maxsplit=1)[0])


def _removeprefix(text: str, /, *, prefix: str) -> str:
    """python 3.8 compatible equivalent to `str.removeprefix()`"""
    if text.startswith(prefix):
        return text[len(prefix) :]
    return text


class Unit(str):
    """https://documentation.ubuntu.com/juju/latest/reference/unit/"""

    @property
    def app(self):
        """The unit's app

        https://documentation.ubuntu.com/juju/latest/reference/application/
        """
        app_, _ = self.split("/")
        return app_

    @property
    def number(self):
        """The unit's number"""
        _, number_ = self.split("/")
        return int(number_)

    def __repr__(self):
        return f"{type(self).__name__}({repr(str(self))})"

    def __lt__(self, other):
        if not isinstance(other, Unit):
            raise TypeError(
                f"'<' not supported between instances of {repr(type(self).__name__)} and {repr(type(other).__name__)}"
            )
        if self.app != other.app:
            raise ValueError(
                f"Unable to compare units with different apps: {repr(self.app)} and {repr(other.app)} ({repr(self)} and {repr(other)})"
            )
        return self.number < other.number

    def __le__(self, other):
        if not isinstance(other, Unit):
            raise TypeError(
                f"'<=' not supported between instances of {repr(type(self).__name__)} and {repr(type(other).__name__)}'"
            )
        if self.app != other.app:
            raise ValueError(
                f"Unable to compare units with different apps: {repr(self.app)} and {repr(other.app)} ({repr(self)} and {repr(other)})"
            )
        return self.number <= other.number

    def __gt__(self, other):
        if not isinstance(other, Unit):
            raise TypeError(
                f"'>' not supported between instances of {repr(type(self).__name__)} and {repr(type(other).__name__)}"
            )
        if self.app != other.app:
            raise ValueError(
                f"Unable to compare units with different apps: {repr(self.app)} and {repr(other.app)} ({repr(self)} and {repr(other)})"
            )
        return self.number > other.number

    def __ge__(self, other):
        if not isinstance(other, Unit):
            raise TypeError(
                f"'>=' not supported between instances of {repr(type(self).__name__)} and {repr(type(other).__name__)}"
            )
        if self.app != other.app:
            raise ValueError(
                f"Unable to compare units with different apps: {repr(self.app)} and {repr(other.app)} ({repr(self)} and {repr(other)})"
            )
        return self.number >= other.number


class _Databag(typing.Mapping[str, str]):
    def __init__(self, *, relation_id: int, unit_or_app: str):
        self._relation_id = relation_id
        self._unit_or_app = unit_or_app

    def __repr__(self):
        return f"{type(self).__name__}(relation_id={self._relation_id}, unit_or_app={repr(self._unit_or_app)})"

    def _command_get(self, *, key: str) -> typing.List[str]:
        """relation-get hook tool command"""
        command = [
            "relation-get",
            "--format",
            "json",
            "--relation",
            str(self._relation_id),
            key,
            self._unit_or_app,
        ]
        if "/" not in self._unit_or_app:
            # `self._unit_or_app` is app
            command.append("--app")
        return command

    def __getitem__(self, key: str) -> str:
        result = json.loads(
            subprocess.run(
                self._command_get(key=key), capture_output=True, check=True, text=True
            ).stdout
        )
        if result is None:
            raise KeyError(key)
        return result

    def __iter__(self):
        result: typing.Dict[str, str] = json.loads(
            subprocess.run(
                self._command_get(key="-"), capture_output=True, check=True, text=True
            ).stdout
        )
        return iter(result.keys())

    def __len__(self):
        result: typing.Dict[str, str] = json.loads(
            subprocess.run(
                self._command_get(key="-"), capture_output=True, check=True, text=True
            ).stdout
        )
        return len(result)


class _WriteableDatabag(_Databag, typing.MutableMapping[str, str]):
    def __setitem__(self, key: str, value: typing.Optional[str]):
        command = ["relation-set", "--relation", str(self._relation_id), "--file", "-"]
        if "/" not in self._unit_or_app:
            # `self._unit_or_app` is app
            command.append("--app")
        subprocess.run(command, input=json.dumps({key: value}), check=True, text=True)
        logger.debug(f"Set {repr(self)}[{repr(key)}] = {repr(value)}")

    def __delitem__(self, key):
        self.__setitem__(key, None)


class _RelationSubset(typing.Mapping[str, typing.Mapping[str, str]]):
    """Lazy loaded read-only mapping for subset of a `Relation`"""

    def __init__(self, *, relation: "Relation", keys: typing.List[str]):
        self._relation = relation
        self._keys = keys

    def __repr__(self):
        return f"{type(self).__name__}(relation={repr(self._relation)}, keys={repr(self._keys)})"

    def __getitem__(self, key):
        if key not in self._keys:
            raise KeyError(key)
        return self._relation[key]

    def __iter__(self):
        return iter(self._keys)

    def __len__(self):
        return len(self._keys)


class Relation(typing.Mapping[str, typing.Mapping[str, str]]):
    """https://documentation.ubuntu.com/juju/latest/reference/relation/"""

    @property
    def _other_units(self):
        return [
            Unit(unit_name)
            for unit_name in json.loads(
                subprocess.run(
                    ["relation-list", "--format", "json", "--relation", str(self.id)],
                    capture_output=True,
                    check=True,
                    text=True,
                ).stdout
            )
        ]

    @property
    def _other_app(self) -> str:
        # TODO: make public and rename to other_app_name?
        return json.loads(
            subprocess.run(
                ["relation-list", "--format", "json", "--relation", str(self.id), "--app"],
                capture_output=True,
                check=True,
                text=True,
            ).stdout
        )

    @property
    def _units_and_apps(self) -> typing.Tuple[str, ...]:
        units_and_apps = [unit()]  # This unit
        if is_leader():
            # In a peer relation, this unit's app will be added later regardless of `is_leader()`
            units_and_apps.append(app())  # This unit's app
        units_and_apps.extend(self._other_units)
        # In a peer relation, `self._other_app` is this unit's app
        units_and_apps.append(self._other_app)
        # Remove duplicates while preserving order
        return tuple(dict.fromkeys(units_and_apps))

    def __init__(self, id_: int, /):
        self._id = id_

    def __eq__(self, other):
        return isinstance(other, Relation) and self.id == other.id

    def __repr__(self):
        return f"{type(self).__name__}({self.id})"

    def __getitem__(self, key):
        if key not in self._units_and_apps:
            if key == app():
                raise KeyError(f"{repr(key)} (this unit is not leader)")
            else:
                raise KeyError(key)
        if key == unit() or (key == app() and is_leader()):
            return _WriteableDatabag(relation_id=self.id, unit_or_app=key)
        return _Databag(relation_id=self.id, unit_or_app=key)

    def __iter__(self):
        return iter(self._units_and_apps)

    def __len__(self):
        return len(self._units_and_apps)

    @property
    def id(self):
        """The relation's ID

        This ID is unique within a model

        For cross-model relations, the same relation may have a different ID for each model

        https://documentation.ubuntu.com/juju/latest/reference/relation/#relation-identification
        """
        return self._id

    @property
    def my_unit(self) -> typing.MutableMapping[str, str]:
        """This unit's data"""
        return self[unit()]

    # TODO: add setter for my_unit (but don't override databag keys that Juju sets automatically)

    @property
    def my_app_rw(self) -> typing.Optional[typing.MutableMapping[str, str]]:
        """This app's data (read-write)

        `None` if this unit is not leader
        """
        try:
            data = self[app()]
        except KeyError:
            return None
        if isinstance(data, collections.abc.MutableMapping):
            return data
        return None

    # TODO: add setter for my_app_rw

    @property
    def other_units(self) -> typing.Mapping[Unit, typing.Mapping[str, str]]:
        """Other units' data

        In a non-peer relation, this is the data of the other app's units
        In a peer relation, this is the data of this app's units, excluding this unit

        In a subordinate (non-peer) relation, this data only includes the other app's unit that is
        deployed to the same machine as this unit
        Note: subordinate charms can have non-subordinate relations and principal charms can have
        subordinate relations
        """
        return _RelationSubset(relation=self, keys=self._other_units)

    @property
    def other_app(self) -> typing.Mapping[str, str]:
        """Other app's data"""
        return self[self._other_app]


class Endpoint(typing.Collection[Relation]):
    """Relation endpoint"""

    # Convenience for subclasses
    _Relation: typing.Type[Relation] = Relation

    @property
    def _relations(self):
        # Example: ["database:5", "database:6"]
        result: typing.List[str] = json.loads(
            subprocess.run(
                ["relation-ids", "--format", "json", self._name],
                capture_output=True,
                check=True,
                text=True,
            ).stdout
        )
        ids = (int(_removeprefix(id_, prefix=f"{self._name}:")) for id_ in result)
        return [self._Relation(id_) for id_ in ids]

    def __init__(self, name: str, /):
        self._name = name

    def __eq__(self, other):
        return isinstance(other, Endpoint) and self._name == other._name

    def __repr__(self):
        return f"{type(self).__name__}({repr(self._name)})"

    def __contains__(self, item):
        return item in self._relations

    def __iter__(self):
        return iter(self._relations)

    def __len__(self):
        return len(self._relations)

    @property
    def relation(self) -> typing.Optional[Relation]:
        """Assume 0 or 1 relations exist on the endpoint & return the relation if it exists

        Should only be used if `limit: 1` is present for the endpoint in metadata.yaml or
        charmcraft.yaml

        Raises `ValueError` if more than 1 relation exists on the endpoint
        """
        if len(self) > 1:
            raise ValueError(
                f"{len(self)} relations on {repr(self)}. `Endpoint.relation` expects 0 or 1 relations"
            )
        for relation in self:
            return relation
        return None


class PeerRelation(Relation):
    """https://documentation.ubuntu.com/juju/latest/reference/relation/#peer"""

    @classmethod
    def from_endpoint(
        cls, endpoint: typing.Union[str, Endpoint], /
    ) -> typing.Optional["PeerRelation"]:
        """Get the peer relation for the endpoint, if the relation exists

        For a peer endpoint, there is a maximum of 1 relation
        """
        if isinstance(endpoint, str):
            endpoint = Endpoint(endpoint)
        if relation := endpoint.relation:
            return cls(relation.id)
        return None

    @property
    def all_units(self) -> typing.Mapping[Unit, typing.Mapping[str, str]]:
        """All units' data

        Includes this unit's data
        """
        return _RelationSubset(relation=self, keys=[unit(), *self._other_units])

    @property
    def my_app_ro(self) -> typing.Mapping[str, str]:
        """This app's data (read-only)"""
        return self.other_app

    @property
    def other_app(self) -> typing.Mapping[str, str]:
        """This app's data

        In a peer relation, the "other" app is this unit's app

        Same as `my_app_ro`
        """
        return super().other_app


class _Config(typing.Mapping[str, typing.Union[str, int, float, bool]]):
    # TODO: add support for secrets
    def __repr__(self):
        return f"{type(self).__name__}()"

    def __getitem__(self, key: str):
        result = json.loads(
            subprocess.run(
                ["config-get", "--format", "json", key], capture_output=True, check=True, text=True
            ).stdout
        )
        if result is None:
            raise KeyError(key)
        return result

    def __iter__(self):
        result: typing.Dict[str, typing.Union[str, int, float, bool]] = json.loads(
            subprocess.run(
                ["config-get", "--format", "json"], capture_output=True, check=True, text=True
            ).stdout
        )
        return iter(result.keys())

    def __len__(self):
        result: typing.Dict[str, typing.Union[str, int, float, bool]] = json.loads(
            subprocess.run(
                ["config-get", "--format", "json"], capture_output=True, check=True, text=True
            ).stdout
        )
        return len(result)


# TODO: add pebble, secret, and storage events
class Event:
    """Juju event

    Also referred to as a "hook"

    https://documentation.ubuntu.com/juju/latest/reference/hook/
    """

    def __repr__(self):
        return f"{type(self).__name__}()"


class ConfigChangedEvent(Event):
    """https://documentation.ubuntu.com/juju/latest/reference/hook/#config-changed"""


class InstallEvent(Event):
    """https://documentation.ubuntu.com/juju/latest/reference/hook/#install"""


class LeaderElectedEvent(Event):
    """https://documentation.ubuntu.com/juju/latest/reference/hook/#leader-elected"""


class LeaderSettingsChangedEvent(Event):
    """https://documentation.ubuntu.com/juju/latest/reference/hook/#leader-settings-changed"""


class PostSeriesUpgradeEvent(Event):
    """https://documentation.ubuntu.com/juju/latest/reference/hook/#post-series-upgrade"""


class PreSeriesUpgradeEvent(Event):
    """https://documentation.ubuntu.com/juju/latest/reference/hook/#pre-series-upgrade"""


class RemoveEvent(Event):
    """https://documentation.ubuntu.com/juju/latest/reference/hook/#remove"""


class StartEvent(Event):
    """https://documentation.ubuntu.com/juju/latest/reference/hook/#start"""


class StopEvent(Event):
    """https://documentation.ubuntu.com/juju/latest/reference/hook/#stop"""


class UpdateStatusEvent(Event):
    """https://documentation.ubuntu.com/juju/latest/reference/hook/#update-status"""


class UpgradeCharmEvent(Event):
    """https://documentation.ubuntu.com/juju/latest/reference/hook/#upgrade-charm"""


_ActionResult = typing.Mapping[str, typing.Union[str, "_ActionResult"]]


class ActionEvent(Event):
    """https://documentation.ubuntu.com/juju/latest/reference/action/#action-execution"""

    @property
    def action(self) -> str:
        return os.environ["JUJU_ACTION_NAME"]

    @property
    def parameters(self) -> collections.abc.Mapping:
        return types.MappingProxyType(
            json.loads(
                subprocess.run(
                    ["action-get", "--format", "json"], capture_output=True, check=True, text=True
                ).stdout
            )
        )

    @staticmethod
    def log(message: str, /):
        subprocess.run(["action-log", message], check=True)

    @classmethod
    def _flatten(cls, old: _ActionResult, /, *, prefix: str = "") -> typing.Mapping[str, str]:
        new = {}
        for key, value in old.items():
            if not isinstance(key, str):
                raise TypeError(
                    f"expected key with type 'str', got {repr(type(key).__name__)}: {repr(key)}"
                )
            for invalid_character in (".", "="):
                if invalid_character in key:
                    raise ValueError(
                        f"{repr(invalid_character)} character not allowed in key: {repr(key)}"
                    )
            if prefix:
                key = f"{prefix}.{key}"
            if isinstance(value, collections.abc.Mapping):
                new.update(cls._flatten(value, prefix=key))
            elif isinstance(value, str):
                new[key] = value
            else:
                raise TypeError(
                    f"expected value with type 'str' or 'collections.abc.Mapping', got {repr(type(value).__name__)}: {repr(value)}"
                )
        return new

    def _set_result(self, value: _ActionResult, /):
        # TODO docstring: add note about how values are merged if called multiple times
        # TODO docstring: "." and "=" characters not allowed in keys (and other hook tool restrictions)
        # TODO: character limit of shell?
        command = ["action-set"]
        for key, value_ in self._flatten(value).items():
            command.append(f"{key}={value_}")
        subprocess.run(command, check=True)
        logger.debug(f"Set {repr(self)}.result = {repr(value)}")

    result = property(fset=_set_result)

    def fail(self, message: str = None, /):
        command = ["action-fail"]
        if message is not None:
            command.append(message)
        subprocess.run(command, check=True)
        logger.debug(f"Called {repr(self)}.fail({repr(message) if message is not None else ''})")


class RelationEvent(Event):
    @property
    def relation(self) -> Relation:
        # Example: "database:5"
        id_ = os.environ["JUJU_RELATION_ID"]
        # Example: 5
        id_ = int(_removeprefix(id_, prefix=f"{os.environ['JUJU_RELATION']}:"))
        relation = Relation(id_)
        # Use `relation._other_app` instead of `os.environ["JUJU_REMOTE_APP"]` because of
        # https://bugs.launchpad.net/juju/+bug/1960934
        if relation._other_app == app():
            return PeerRelation(id_)
        return relation

    @property
    def endpoint(self) -> Endpoint:
        return Endpoint(os.environ["JUJU_RELATION"])


class RelationBrokenEvent(RelationEvent):
    """https://documentation.ubuntu.com/juju/latest/reference/hook/#endpoint-relation-broken"""


class RelationCreatedEvent(RelationEvent):
    """https://documentation.ubuntu.com/juju/latest/reference/hook/#endpoint-relation-created"""


class _RelationUnitEvent(RelationEvent):
    @property
    def remote_unit(self) -> Unit:
        return Unit(os.environ["JUJU_REMOTE_UNIT"])


class RelationChangedEvent(_RelationUnitEvent):
    """https://documentation.ubuntu.com/juju/latest/reference/hook/#endpoint-relation-changed"""


class RelationDepartedEvent(_RelationUnitEvent):
    """https://documentation.ubuntu.com/juju/latest/reference/hook/#endpoint-relation-departed"""

    @property
    def departing_unit(self) -> Unit:
        return Unit(os.environ["JUJU_DEPARTING_UNIT"])


class RelationJoinedEvent(_RelationUnitEvent):
    """https://documentation.ubuntu.com/juju/latest/reference/hook/#endpoint-relation-joined"""


class _UnknownEvent(Event):
    """Temporary placeholder while not all Juju events are implemented

    (e.g. pebble, secret, and storage events)
    """


def set_app_workload_version(version: str, /) -> None:
    """Set the workload version displayed in `juju status` for this app"""
    subprocess.run(["application-version-set", version], check=True)
    logger.debug(f"Called set_app_workload_version({repr(version)})")


def unit():
    return Unit(os.environ["JUJU_UNIT_NAME"])


def app():
    return unit().app


def model():
    return os.environ["JUJU_MODEL_NAME"]


def is_leader() -> bool:
    return json.loads(
        subprocess.run(
            ["is-leader", "--format", "json"], capture_output=True, check=True, text=True
        ).stdout
    )


def event() -> Event:
    if os.environ.get("JUJU_ACTION_NAME"):
        return ActionEvent()
    name = os.environ["JUJU_HOOK_NAME"]
    try:
        return _STATICALLY_NAMED_EVENT_TYPES[name]()
    except KeyError:
        pass
    for suffix, type_ in _DYNAMICALLY_NAMED_EVENT_TYPES.items():
        if name.endswith(suffix):
            return type_()
    # TODO: add pebble, secret, and storage events
    return _UnknownEvent()


_STATICALLY_NAMED_EVENT_TYPES: typing.Dict[str, typing.Type[Event]] = {
    "config-changed": ConfigChangedEvent,
    "install": InstallEvent,
    "leader-elected": LeaderElectedEvent,
    "leader-settings-changed": LeaderSettingsChangedEvent,
    "post-series-upgrade": PostSeriesUpgradeEvent,
    "pre-series-upgrade": PreSeriesUpgradeEvent,
    "remove": RemoveEvent,
    "start": StartEvent,
    "stop": StopEvent,
    "update-status": UpdateStatusEvent,
    "upgrade-charm": UpgradeCharmEvent,
}
_DYNAMICALLY_NAMED_EVENT_TYPES: typing.Dict[str, typing.Type[Event]] = {
    "-relation-broken": RelationBrokenEvent,
    "-relation-changed": RelationChangedEvent,
    "-relation-created": RelationCreatedEvent,
    "-relation-departed": RelationDepartedEvent,
    "-relation-joined": RelationJoinedEvent,
}
