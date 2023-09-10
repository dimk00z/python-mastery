import decimal
import inspect
from functools import wraps


class Validator:
    validators = {}

    def __init__(self, name=None):
        self.name = name

    def __set_name__(self, cls, name):
        self.name = name

    @classmethod
    def check(cls, value):
        return value

    def __set__(self, instance, value):
        instance.__dict__[self.name] = self.check(value)

    @classmethod
    def __init_subclass__(cls):
        cls.validators[cls.__name__] = cls


class Typed(Validator):
    expected_type = object

    @classmethod
    def check(cls, value):
        if not isinstance(value, cls.expected_type):
            raise TypeError(f"Expected {cls.expected_type}")
        return super().check(value)


_typed_classes = [
    ("Integer", int),
    ("Float", float),
    ("Complex", complex),
    ("Decimal", decimal.Decimal),
    ("List", list),
    ("Bool", bool),
    ("String", str),
]
globals().update(
    (name, type(name, (Typed,), {"expected_type": ty})) for name, ty in _typed_classes
)


# class Integer(Typed):
#     expected_type = int


# class Float(Typed):
#     expected_type = float


# class String(Typed):
#     expected_type = str


class Positive(Validator):
    @classmethod
    def check(cls, value):
        if value < 0:
            raise ValueError("Expected >= 0")
        return super().check(value)


class NonEmpty(Validator):
    @classmethod
    def check(cls, value):
        if len(value) == 0:
            raise ValueError("Must be non-empty")
        return super().check(value)


class PositiveInteger(Integer, Positive):
    pass


class PositiveFloat(Float, Positive):
    pass


class NonEmptyString(String, NonEmpty):
    pass


def validated(func):
    signature = inspect.signature(func)
    annotations = dict(func.__annotations__)
    retcheck = annotations.pop("return", None)

    @wraps(func)
    def wrapper(*args, **kwargs):
        bound = signature.bind(*args, **kwargs)
        errors = []

        # Enforce argument checks
        for name, validator in annotations.items():
            try:
                validator.check(bound.arguments[name])
            except Exception as e:
                errors.append(f"    {name}: {e}")

        if errors:
            raise TypeError("Bad Arguments\n" + "\n".join(errors))

        result = func(*args, **kwargs)

        # Enforce return check (if any)
        if retcheck:
            try:
                retcheck.check(result)
            except Exception as e:
                raise TypeError(f"Bad return: {e}") from None
        return result

    return wrapper


def enforce(**annotations):
    retcheck = annotations.pop("return_", None)

    def decorate(func):
        sig = inspect.signature(func)

        @wraps(func)
        def wrapper(*args, **kwargs):
            bound = sig.bind(*args, **kwargs)
            errors = []

            # Enforce argument checks
            for name, validator in annotations.items():
                try:
                    validator.check(bound.arguments[name])
                except Exception as e:
                    errors.append(f"    {name}: {e}")

            if errors:
                raise TypeError("Bad Arguments\n" + "\n".join(errors))

            result = func(*args, **kwargs)

            if retcheck:
                try:
                    retcheck.check(result)
                except Exception as e:
                    raise TypeError(f"Bad return: {e}") from None
            return result

        return wrapper

    return decorate


if __name__ == "__main__":

    @validated
    def add(x: Integer, y: Integer) -> Integer:
        return x + y
