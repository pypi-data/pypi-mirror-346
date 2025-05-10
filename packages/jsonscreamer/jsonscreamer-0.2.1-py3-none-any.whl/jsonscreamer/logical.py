"""Logical combinators and modifiers of schemas."""

from __future__ import annotations

from typing import TYPE_CHECKING

from .compile import compile_ as _compile, register as _register
from .types import ValidationError

if TYPE_CHECKING:
    from .types import Context, Schema, Validator


@_register
def not_(defn: Schema, context: Context) -> Validator:
    validator = _compile(defn["not"], context)

    def validate(x, path):
        if not validator(x, path):
            return ValidationError(path, f"{x} should not satisfy {defn['not']}", "not")

    return validate


@_register
def all_of(defn: Schema, context: Context) -> Validator:
    validators = [_compile(s, context) for s in defn["allOf"]]

    def validate(x, path):
        for v in validators:
            err = v(x, path)
            if err:
                return err

    return validate


@_register
def any_of(defn: Schema, context: Context) -> Validator:
    validators = [_compile(s, context) for s in defn["anyOf"]]

    def validate(x, path):
        messages = []
        for v in validators:
            err = v(x, path)
            if err is None:
                return None
            messages.append(err.message)

        failures = ", ".join(messages)
        return ValidationError(path, f"{x} failed all conditions: {failures}", "anyOf")

    return validate


@_register
def one_of(defn: Schema, context: Context) -> Validator:
    validators = [_compile(s, context) for s in defn["oneOf"]]

    def validate(x, path):
        passed = 0

        for v in validators:
            err = v(x, path)
            if err is None:
                passed += 1

        if passed != 1:
            return ValidationError(
                path, f"{x} satisfied {passed} (!= 1) of the conditions", "oneOf"
            )

    return validate


@_register
def if_(defn: Schema, context: Context) -> Validator | None:
    if_schema = defn["if"]
    then_schema = defn.get("then", True)
    else_schema = defn.get("else", True)

    if then_schema is True and else_schema is True:
        return None

    if_validator = _compile(if_schema, context)
    then_validator = _compile(then_schema, context)
    else_validator = _compile(else_schema, context)

    def validate(x, path):
        if not if_validator(x, path):  # XXX: no errors => if condition true
            return then_validator(x, path)
        return else_validator(x, path)

    return validate
