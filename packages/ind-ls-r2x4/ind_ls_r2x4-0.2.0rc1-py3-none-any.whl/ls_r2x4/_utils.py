import abc
import weakref

from typing import Any, Callable, List, Optional


class ConfigError(ValueError):
    pass


class ConfigOptionsError(ConfigError):
    pass


class ConfigTypeError(ConfigError):
    pass


class ConfigRangeError(ConfigError):
    pass


class _ConfigItem:
    TYPE = None

    def __init__(self, name, gui_show=True, options=None, doc=None):
        self.name = name
        self._gui_show = gui_show
        self._value = None
        self.touched = False
        self.options = options
        self.doc = doc
        self._actions = dict()  # dict with actions to be made available in the gui (ex. direct write)
        self.set_value_event = Event()
        self._locked = True

    def __setattr__(self, name, value):
        """Protect setting attributes different from 'value' to a config item"""
        if name == 'value':
            self.set_value(value)
        else:
            if getattr(self, "_locked", None) and name not in ('touched', '_value', 'set_value_event'):
                raise AttributeError("No attributes can be added to Config Items")
            self.__dict__[name] = value

    @property
    def value(self):
        """Get the value of the config"""
        return self._value

    @value.setter
    def value(self, value):
        """Check and set the value of the config"""
        # this code will never be reached because __setattr__ is overwritten,
        # but it is left in here for readability and IDE code inspection
        self.set_value(value)

    def set_value(self, value, trigger_event: bool = True):
        """Check and set the value of the config

        Pulled out of the property setter to be able to call it from the overwritten __setattr__ method.

        :param value: to be set
        :param trigger_event: defines if the event should be triggered
        """
        self._value = self._check_and_convert(value)
        self.touched = True
        if trigger_event:
            # notify any listeners
            self.set_value_event(self)

    def _check_and_convert(self, value):
        """Check type and options value of the config"""
        if not issubclass(type(value), self.TYPE):
            try:
                value = self.TYPE(value)
            except ValueError:
                raise ConfigTypeError(f"Value of config type '{type(self).__name__}' is different from supported types, "
                                      f"'{type(value)}' vs '{self.TYPE}'")
        self._check_options(value)
        return value

    def _check_options(self, value):
        if self.options is not None:
            if value not in self.options:
                raise ConfigOptionsError(f"Value of config type '{type(self).__name__}': '{value}' is not found in "
                                         f"options: '{self.options}'")

    def __str__(self):
        s = type(self).__name__
        try:
            s += f" / TYPE: {self.TYPE.__name__}"
        except AttributeError:
            s += f" / TYPE: {self.TYPE}"
        s += f" / value: {self.value}"
        if self.options:
            s += f" / OPTIONS: {self.options}"
        return s

    def __repr__(self):
        return self.__str__()


class ConfigBool(_ConfigItem):
    TYPE = bool

    def __init__(self, name, doc=None, gui_show=True):
        super().__init__(name, gui_show, doc=doc, options=(True, False))


class ConfigValue(_ConfigItem, abc.ABC):

    def __init__(self, name, gui_show=True, options=None, doc=None, unit=None, minimum=None, maximum=None):
        self.unit = unit
        self.min = minimum
        self.max = maximum
        super().__init__(name, gui_show, options, doc)

    def _check_and_convert(self, value):
        """Check if value matches the type, options and range

        Convert the value to the correct type if possible / needed and return it.
        """
        value = super()._check_and_convert(value)
        self._check_range(value)
        return value

    def _check_range(self, value):
        """Check if the value is within range"""
        if self.min is not None:
            if not value >= self.min:
                raise ConfigRangeError(f"Config {type(self).__name__} is too low, {value} < {self.min}")
        if self.max is not None:
            if not value <= self.max:
                raise ConfigRangeError(f"Config {type(self).__name__} is too high, {value} > {self.max}")

    def __str__(self):
        s = super().__str__()
        if self.min is not None:
            s += f" / min: {self.min}"
        if self.max is not None:
            s += f" / max: {self.max}"
        if self.unit is not None:
            s += f" / unit: {self.unit}"
        return s


class ConfigFloat(ConfigValue):
    TYPE = float

    def _check_and_convert(self, value):
        """ Both int and float are ok when a float is expected """
        if type(value) not in (int, float) and not issubclass(type(value), self.TYPE):
                try:
                    value = float(value)
                except ValueError:
                    raise ConfigTypeError(f"Value of config type '{type(self).__name__}' is different from supported "
                                          f"types, '{type(value)}' vs 'float or int'")
        self._check_options(value)
        self._check_range(value)
        return value


class Event:
    """
    Dispatch function calls to multiple event handler methods.

    Calls are handled by __call__ and accept arbitrary positional
    and keyword arguments.  Each handler receives the same arguments.

    If keyword arguments are given in the constructor, then position
    args are not allowed and the keyword arguments of each call
    must match.

    Use weak references to not keep the handlers alive when not required.
    Deleted handlers are cleaned up whenever the event is called.

    Handlers are added with `+=` and removed with `-=`.
    They are called in the order of registration.
    """

    def __init__(self, *argument_names) -> None:
        """
        Initialize the Event object.

        :param argument_names: Names of arguments that the event
            passes on to its handlers.
        """
        self._handlers: List[weakref.ReferenceType[Callable]] = []
        self._argument_names = set(argument_names)

    def add(self, handler: Callable):
        """
        Add a handler.

        Use this method instead of `+=` syntax when the
        event is exposed through a read-only property (no setter).

        :raises ValueError: When the handler is already added.
        :param handler: The handler to add.
        """
        if handler in self:
            raise ValueError("Handler already present")

        # check if it is a bound method, in which case we need to use WeakMethod
        if hasattr(handler, '__self__'):
            self._handlers.append(weakref.WeakMethod(handler))
        else:
            self._handlers.append(weakref.ref(handler))

    def __bool__(self) -> bool:
        """
        Return whether the event has any handlers.

        :returns: True when one or more handlers are present.
        """
        return len(self) > 0

    def __len__(self) -> int:
        """
        Return the count of handlers.The handler to add.

        :returns: Number of handlers.
        """
        self._drop_dead_handlers()
        return len(self._handlers)

    def __iadd__(self, handler: Callable) -> "Event":
        """
        Add a handler and return the event.

        :raises ValueError: When the handler is already added.
        :param handler: The handler to add.
        :returns: self.
        """
        self.add(handler)
        return self

    def __isub__(self, handler: Callable) -> "Event":
        """
        Remove a handler.

        :param handler: The handler to remove.
        :returns: self.
        """
        self._remove(handler)
        return self

    def __contains__(self, handler: Callable) -> bool:
        """
        Return whether the event contains the given handler.

        :param handler: The handler callable to search for.
        :returns: True if the handler is present; False otherwise.
        """
        index = self._find(handler)
        return index is not None

    def __call__(self, *args: Any, **kwargs: Any) -> None:
        """
        Dispatch the function call to all handlers.

        :param args: Positional arguments.
        :param kwargs: Keyword arguments.
        """
        if self._argument_names and not set(kwargs.keys()) == self._argument_names:
            raise ValueError(
                f"Keywords don't match for event call: {set(kwargs.keys())!r}"
                f" vs {self._argument_names!r}."
            )
        if self._argument_names and args:
            raise ValueError(
                f"Positional arguments are not allowed for event defined with keywords: {args!r}."
            )

        cleanup_required = False

        for weak_handler in self._handlers:
            handler = weak_handler()
            if handler is None:
                cleanup_required = True
                continue
            handler(*args, **kwargs)

        if cleanup_required:
            self._drop_dead_handlers()

    def __delitem__(self, handler: Callable) -> None:
        """
        Remove the given handler.

        :param handler: The handler to remove.
        """
        self._remove(handler)

    def __repr__(self):
        """
        Return a structured string representation.

        :returns: String like "Event(handlers=[...])".
        """
        return f"Event(handlers={repr(self._handlers)})"

    def __str__(self):
        """
        Return a readable string representation.

        :returns: String like "Event".
        """
        return "Event"

    def _drop_dead_handlers(self) -> None:
        """Remove all handlers whose weak reference is dead (produces None)."""
        self._handlers = [
            handler for handler in self._handlers if handler() is not None
        ]

    def _remove(self, handler: Callable) -> None:
        """
        Remove the given handler's reference.

        :param handler: Handler to remove.
        :raises ValueError: When the handler can't be found.
        """
        index = self._find(handler)
        if index is None:
            raise ValueError("Handler is not present")

        self._handlers = self._handlers[0:index] + self._handlers[index + 1 :]

    def _find(self, handler: Callable) -> Optional[int]:
        """
        Return the index of the given handler (if any).

        :param handler: The handler to search.
        :returns: None or the index of the found handler.
        """
        for i, weak_handler in enumerate(self._handlers):
            if handler == weak_handler():
                return i

        return None


class R2X4OperationError(Exception):
    """Exception raised for issues related with the R2X4 light source."""
    def __init__(self, message: str = "An issue was detected with the R2X4 light source"):
        super().__init__(message)
