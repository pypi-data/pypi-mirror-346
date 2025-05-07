from abc import ABCMeta
from typing import Any, Dict, List, Tuple, Type
import itertools as it

from .errors import InheritanceError
from .impl import Impl
from .struct import Struct


class EnumVariantInstance:
    """
    Represents an instance of a constructor variant in an oxitrait Enum.
    Created when calling a variant like Paint.CUSTOM(...).
    """

    __slots__ = ("_enum_cls", "_variant", "_payload")

    def __init__(self, enum_cls: type, variant: str, payload: Any = None):
        self._enum_cls = enum_cls
        self._variant = variant
        self._payload = payload

    def __repr__(self):
        if self._payload is None:
            return f"<{self._enum_cls.__name__}.{self._variant}>"
        return f"<{self._enum_cls.__name__}.{self._variant} payload={self._payload!r}>"

    def __eq__(self, other):
        return (
            isinstance(other, EnumVariantInstance)
            and self._enum_cls is other._enum_cls
            and self._variant == other._variant
            and self._payload == other._payload
        )

    def __hash__(self):
        return hash((self._enum_cls, self._variant, self._payload))

    def __getattr__(self, name):
        if self._payload is not None:
            return getattr(self._payload, name)
        raise AttributeError(f"{self!r} has no attribute {name!r}")

    def __match_args__(self):
        return ("variant",)

    @property
    def variant(self):
        return self._variant

    @property
    def enum(self):
        return self._enum_cls

    @property
    def payload(self):
        return self._payload


class EnumVariant:
    """
    Represents a single variant of an oxitrait Enum.
    Variants are created automatically by the Enum metaclass and exposed as attributes.
    """

    __slots__ = ("_enum_cls", "_name", "_struct_cls")

    def __init__(self, enum_cls: Type, name: str, struct_cls: Type | None = None):
        self._enum_cls = enum_cls
        self._name = name
        self._struct_cls = struct_cls

    def __call__(self, *args, **kwargs):
        if self._struct_cls is not None:
            # Constructor variant with Struct payload
            payload = self._struct_cls(*args, **kwargs)
        else:
            if args or kwargs:
                raise TypeError(f"{self._name} is a unit variant and does not take arguments")
            payload = None

        return EnumVariantInstance(self._enum_cls, self._name, payload)

    def __str__(self):
        return self._name

    def __repr__(self):
        return f"<{self._enum_cls.__name__}.{self._name}>"

    def __eq__(self, other):
        return (
            isinstance(other, EnumVariant)
            and self._enum_cls is other._enum_cls
            and self._name == other._name
        )

    def __hash__(self):
        return hash((self._enum_cls, self._name))

    @property
    def name(self):
        """Returns the name of this enum variant, as a string."""
        return self._name

    @property
    def enum(self):
        """Returns the parent enum class this variant belongs to."""
        return self._enum_cls

    def __getattr__(self, attr: str):
        """
        Resolves missing attributes by lazily injecting trait methods from Impl blocks
        into the enum class, then binding and returning the requested method.
        """
        if not hasattr(self._enum_cls, attr):
            from .impl import Impl
            impl_bases = Impl.registry.get(self._enum_cls.__name__, [])
            for base in impl_bases:
                for name in dir(base):
                    if name.startswith("__"):
                        continue
                    value = getattr(base, name)
                    if callable(value) and not hasattr(self._enum_cls, name):
                        setattr(self._enum_cls, name, value)

        method = getattr(self._enum_cls, attr)
        if callable(method):
            return method.__get__(self, type(self))
        return method


class Enum(ABCMeta):
    """
    Metaclass for defining oxitrait Enums.

    Use `metaclass=Enum` to define a trait-aware enum. Variants are declared using
    `auto()`. Trait implementations for the enum are automatically injected via
    Impl blocks registered using `target="MyEnum"`.

    Example:
        class Color(metaclass=Enum):
            RED = auto()
            BLUE = auto()
    """

    def __new__(mcls, name: str, bases: Tuple[type], attrs: Dict[str, Any], **kwargs):
        if __debug__ and bases:
            raise InheritanceError(f"Enum {name} must have no explicit superclasses.")

        variant_tokens = {k: v for k, v in list(attrs.items()) if isinstance(v, _AutoEnumToken)}
        for key in variant_tokens:
            del attrs[key]

        impl_bases = Impl.registry.get(name, [])
        traits_implemented = set(it.chain.from_iterable(impl.traits() for impl in impl_bases))
        traits_to_check = traits_implemented.copy()

        while traits_to_check:
            trait = traits_to_check.pop()
            blanket = Impl.blanket_registry.get(trait.__name__)
            if not blanket:
                continue
            impl_bases.extend(blanket)
            new_traits = set(it.chain.from_iterable(impl.traits() for impl in blanket))
            traits_implemented.update(new_traits)
            traits_to_check.update(new_traits)

        all_bases = tuple(impl_bases)
        cls = super().__new__(mcls, name, all_bases, attrs)
        cls._variant_names = list(variant_tokens.keys())
        cls._variants: Dict[str, EnumVariant] = {}

        for var_name, token in variant_tokens.items():
            if token.payload_cls is None:
                # Unit variant → instantiate immediately
                instance = EnumVariantInstance(cls, var_name, payload=None)
                cls._variants[var_name] = instance
                setattr(cls, var_name, instance)
            else:
                # Constructor variant → generate callable EnumVariant
                constructor = EnumVariant(cls, var_name, struct_cls=token.payload_cls)
                cls._variants[var_name] = constructor
                setattr(cls, var_name, constructor)


        cls.traits = frozenset(traits_implemented)

        for base in impl_bases:
            for attr in dir(base):
                if attr.startswith("__"):
                    continue
                value = getattr(base, attr)
                if callable(value) and not hasattr(cls, attr):
                    setattr(cls, attr, value)

        ABCMeta.__init__(cls, name, all_bases, attrs)

        return cls

    def __iter__(cls):
        """Iterate over all enum variants."""
        return iter(cls._variants.values())

    def __getitem__(cls, item: str):
        """Access an enum variant by name."""
        return cls._variants[item]

    def __contains__(cls, item: Any):
        """Check if a value is one of the enum's variants."""
        return item in cls._variants.values()

    def variant_names(cls) -> List[str]:
        """Return a list of all variant names, as strings."""
        return list(cls._variant_names)

    def variants(cls) -> List[EnumVariant]:
        """Return a list of all EnumVariant objects."""
        return list(cls._variants.values())


class _AutoEnumToken:
    def __init__(self, payload_cls: type | None = None):
        self.payload_cls = payload_cls

def auto(arg=None) -> _AutoEnumToken:
    """
    Declare an enum variant.

    - `auto()` -> unit variant
    - `auto(StructClass)` -> constructor variant with typed payload (must be a Struct)

    Raises:
        TypeError if a non-Struct is passed.
    """
    if arg is None:
        return _AutoEnumToken(payload_cls=None)

    if isinstance(arg, type) and issubclass(arg, Struct):
        return _AutoEnumToken(payload_cls=arg)

    raise TypeError(
        f"auto() only supports no arguments (unit variant) or a Struct subclass "
        f"(constructor variant). Got: {arg!r}"
    )
