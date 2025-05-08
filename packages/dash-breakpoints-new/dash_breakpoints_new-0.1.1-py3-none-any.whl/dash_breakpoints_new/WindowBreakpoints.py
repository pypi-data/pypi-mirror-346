# AUTO GENERATED FILE - DO NOT EDIT

import typing  # noqa: F401
from typing_extensions import TypedDict, NotRequired, Literal # noqa: F401
from dash.development.base_component import Component, _explicitize_args

ComponentType = typing.Union[
    str,
    int,
    float,
    Component,
    None,
    typing.Sequence[typing.Union[str, int, float, Component, None]],
]

NumberType = typing.Union[
    typing.SupportsFloat, typing.SupportsInt, typing.SupportsComplex
]


class WindowBreakpoints(Component):
    """A WindowBreakpoints component.
Component description

Keyword arguments:

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- height (number; optional):
    Current height, NOTE: avoid using in a server callback.

- heightBreakpoint (string; optional):
    Current height breakpoint.

- heightBreakpointNames (list of strings; optional):
    Name of each height breakpoint, array of length N + 1.

- heightBreakpointThresholdsPx (list of numbers; optional):
    Window heights on which to separate breakpoints, array of length
    N.

- width (number; optional):
    Current width, NOTE: avoid using in a server callback.

- widthBreakpoint (string; optional):
    Current width breakpoint.

- widthBreakpointNames (list of strings; optional):
    Name of each width breakpoint, array of length N + 1.

- widthBreakpointThresholdsPx (list of numbers; optional):
    Window widths on which to separate breakpoints, array of length N."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_breakpoints_new'
    _type = 'WindowBreakpoints'


    def __init__(
        self,
        widthBreakpointThresholdsPx: typing.Optional[typing.Sequence[NumberType]] = None,
        widthBreakpointNames: typing.Optional[typing.Sequence[str]] = None,
        heightBreakpointThresholdsPx: typing.Optional[typing.Sequence[NumberType]] = None,
        heightBreakpointNames: typing.Optional[typing.Sequence[str]] = None,
        width: typing.Optional[NumberType] = None,
        height: typing.Optional[NumberType] = None,
        widthBreakpoint: typing.Optional[str] = None,
        heightBreakpoint: typing.Optional[str] = None,
        id: typing.Optional[typing.Union[str, dict]] = None,
        **kwargs
    ):
        self._prop_names = ['id', 'height', 'heightBreakpoint', 'heightBreakpointNames', 'heightBreakpointThresholdsPx', 'width', 'widthBreakpoint', 'widthBreakpointNames', 'widthBreakpointThresholdsPx']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'height', 'heightBreakpoint', 'heightBreakpointNames', 'heightBreakpointThresholdsPx', 'width', 'widthBreakpoint', 'widthBreakpointNames', 'widthBreakpointThresholdsPx']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(WindowBreakpoints, self).__init__(**args)

setattr(WindowBreakpoints, "__init__", _explicitize_args(WindowBreakpoints.__init__))
