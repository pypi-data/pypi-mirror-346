import re

from collections.abc import Iterator
from operator import itemgetter
from typing import Any, Union, cast


# typing.Self added in Python 3.11
try:
    from typing import Self
except ImportError:  # pragma: no cover
    from typing_extensions import Self

# typing.TypeAlias added in Python 3.10
try:
    from typing import TypeAlias
except ImportError:  # pragma: no cover
    from typing_extensions import TypeAlias

from public import public


COMMASPACE = ', '
SPACE = ' '
IDENTIFIER_RE = r'^[a-zA-Z_][a-zA-Z0-9_]*$'


# The `type` statement was introduced in Python 3.12.
LookupValue: TypeAlias = Union['EnumValue', str]


class EnumMetaclass(type):
    """Meta class for Enums."""

    def __init__(cls, name: str, bases: tuple[type, ...], namespace: dict[str, Any]):
        """Create an Enum class.

        :param cls: The class being defined.
        :param name: The name of the class.
        :param bases: The class's base classes.
        :param namespace: The class attributes.
        """
        super().__init__(name, bases, namespace)
        # values -> EnumValues
        cls._byvalue = {}
        # Figure out if this class has a custom factory for building enum
        # values.  The default is EnumValue, but the class (or one of its
        # bases) can declare a custom one with a special attribute.
        factory = namespace.get('__value_factory__')
        # Figure out the set of enum values on the base classes, to ensure
        # that we don't get any duplicate values.  At the same time, check the
        # base classes for the special attribute.
        for basecls in cls.__mro__:
            if hasattr(basecls, '_byvalue'):
                cls._byvalue.update(basecls._byvalue)  # noqa: SLF001 - Private member accessed: `_byvalue`
            if hasattr(basecls, '__value_factory__'):
                basecls_factory = basecls.__value_factory__
                if factory is not None and basecls_factory != factory:
                    raise TypeError(f'Conflicting enum factory in base class: {basecls_factory}')
                factory = basecls_factory
        # Set the factory default if necessary.
        if factory is None:
            factory = EnumValue
        # For each class attribute, create an enum value and store that back
        # on the class instead of the original value.  Skip Python reserved
        # names.  Also add a mapping from the original value to the enum value
        # instance so we can return the same object on conversion.
        for attr in namespace:
            if not (attr.startswith('__') and attr.endswith('__')):
                value = namespace[attr]
                enumval = factory(cls, value, attr)
                if value in cls._byvalue:
                    other = cls._byvalue[value]
                    # Without this, sort order is undefined and causes
                    # unpredictable results for the test suite.
                    first = attr if attr < other else other
                    second = other if attr < other else attr
                    raise ValueError(
                        f"Conflicting enum value '{value}' for names: '{first}' and '{second}'"
                    )
                # Store as an attribute on the class, and save the attr name.
                setattr(cls, attr, enumval)
                cls._byvalue[value] = attr

    def __dir__(cls) -> list[str]:
        return list(cls._byvalue.values())

    def __repr__(cls) -> str:
        # We want predictable reprs.  Because base Enum items can have any
        # value, the only reliable way to sort the keys for the repr is based
        # on the attribute name, which must be Python identifiers.
        value = COMMASPACE.join(
            f'{value}: {key}' for key, value in sorted(cls._byvalue.items(), key=itemgetter(1))
        )
        return f'<{cls.__name__} {{{value}}}>'

    def __iter__(cls) -> Iterator['EnumValue']:
        for value in cls._byvalue.values():
            yield getattr(cls, value)

    def __getitem__(cls, item: LookupValue) -> 'EnumValue':
        try:
            return getattr(cls, item)  # type: ignore
        except (AttributeError, TypeError):
            if hasattr(item, 'value'):
                attr = cls._byvalue.get(item.value)
                if attr is None:
                    raise KeyError(item) from None
                return cast(EnumValue, getattr(cls, attr))
            missing = object()
            value = cls._byvalue.get(item, missing)
            if value is not missing:
                return cast(EnumValue, getattr(cls, value))
            raise KeyError(item) from None

    def __call__(cls, *args):  # type: ignore
        if len(args) == 1:
            return cls.__getitem__(args[0])
        # Two argument allows for extending enums.
        name, source = args
        return _make(cls, name, source)


@public
class EnumValue:
    """Class representing an enumeration value.

    EnumValue(Color, 'red', 12) prints as 'Color.red' and can be converted
    to the integer 12.
    """

    def __init__(self, enum: EnumMetaclass, value: Any, name: str):
        self._enum = enum
        self._value = value
        self._name = name

    def __repr__(self) -> str:
        return f'<EnumValue: {self._enum.__name__}.{self._name} [value={self._value}]>'

    def __str__(self) -> str:
        return f'{self._enum.__name__}.{self._name}'

    def __reduce__(self):  # type: ignore
        return getattr, (self._enum, self._name)

    @property
    def enum(self) -> EnumMetaclass:
        """The underlying enum."""
        return self._enum

    @property
    def name(self) -> str:
        """The enum's name."""
        return self._name

    @property
    def value(self) -> Any:
        """The enum's value."""
        return self._value

    # Support only comparison by identity and equality.  Ordered comparisons are not supported.
    def __eq__(self, other: object) -> bool:
        return self is other

    def __ne__(self, other: object) -> bool:
        return self is not other

    def __lt__(self, other: Any) -> Any:
        return NotImplemented

    def __gt__(self, other: Any) -> Any:
        return NotImplemented

    def __le__(self, other: Any) -> Any:
        return NotImplemented

    def __ge__(self, other: Any) -> Any:
        return NotImplemented

    __hash__ = object.__hash__


@public
class Enum(metaclass=EnumMetaclass):
    """The public API Enum class."""


class IntEnumValue(int, EnumValue):
    """An EnumValue that is also an integer."""

    def __new__(
        cls,
        enum: EnumMetaclass,  # noqa: ARG003 Unused class method argument
        value: Any,
        attr: str,  # noqa: ARG003 Unused class method argument
    ) -> Self:
        # `attr` is going to be the attribute name as created through the
        # factory call in EnumMetaclass.__init__(), however we need to throw
        # that away when calling int's __new__().
        return super().__new__(cls, value)

    __repr__ = EnumValue.__repr__
    __str__ = EnumValue.__str__

    # The non-deprecated version of this method.
    def __int__(self) -> int:
        return cast(int, self._value)

    __hash__ = int.__hash__

    # For slices and index().
    __index__ = __int__


class IntEnumMetaclass(EnumMetaclass):
    # Define an iteration over the integer values instead of the attribute names.
    def __iter__(cls) -> Iterator[IntEnumValue]:  # noqa: N805 First argument of a method should be `self`
        for key in cls._byvalue:
            yield getattr(cls, cls._byvalue[key])


@public
class IntEnum(metaclass=IntEnumMetaclass):
    """A specialized enumeration with values that are also integers."""

    __value_factory__ = IntEnumValue


def _swap(sequence: Iterator[Any]) -> Iterator[Any]:
    for key, value in sequence:
        yield value, key


def _make(enum_class: EnumMetaclass, name: str, source: Any) -> EnumMetaclass:
    # The common implementation for Enum() and IntEnum().
    namespace = {}
    illegals = []
    have_strings: bool | None = None
    # Auto-splitting of strings.
    if isinstance(source, str):
        source = source.split()
    # Look for dict-like arguments.  Specifically, it must have a callable
    # .items() attribute.  Because of the way enumerate() works, here we have
    # to swap the key/values.
    try:
        source = _swap(source.items())
    except (TypeError, AttributeError):
        source = enumerate(source, start=1)
    for i, item in source:
        if isinstance(item, str):
            if have_strings is None:
                have_strings = True
            elif not have_strings:
                raise ValueError('heterogeneous source')
            namespace[item] = i
            if re.match(IDENTIFIER_RE, item) is None:
                illegals.append(item)
        else:
            if have_strings is None:
                have_strings = False
            elif have_strings:
                raise ValueError('heterogeneous source')
            item_name, item_value = item
            namespace[item_name] = item_value
            if re.match(IDENTIFIER_RE, item_name) is None:
                illegals.append(item_name)
    if len(illegals) > 0:
        raise ValueError(f'non-identifiers: {SPACE.join(illegals)}')
    return EnumMetaclass(str(name), (enum_class,), namespace)
