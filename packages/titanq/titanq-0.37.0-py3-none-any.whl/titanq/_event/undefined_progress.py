# Copyright (c) 2025, InfinityQ Technology, Inc.

"""
Progress events are some type of events that would occur over a timeline with
some progress updates.
"""

from typing import TypeVar
from typing_extensions import override

from titanq._event import Event, ProgressEvent
from titanq._event.sink import Sink, UndefinedProgress

T = TypeVar('T')


_WAITING_UNDEFINED_PROGRESS_COLOR = "orange3"


class PreparingDataEvent(ProgressEvent):
    """Undefined progress event when the SDK is preparing data."""

    def __init__(self):
        self._undefined_progress: UndefinedProgress = None

    @override
    def start(self, sink: Sink) -> Event:
        self._undefined_progress = sink.undefined_progress()
        content = self._undefined_progress.start_content(
            sink.content_builder()
                .set_color(_WAITING_UNDEFINED_PROGRESS_COLOR)
                .add_emoji(":wrench:")
                .add_whitespace()
                .add_text("Preparing data for TitanQ")
                .build()
        )
        sink.display(content)

    @override
    def end(self, sink: Sink) -> Event:
        sink.display(
            sink.content_builder()
                .add_emoji(":wrench:")
                .add_whitespace()
                .add_text("Data prepared for TitanQ")
                .build()
        )


class SendingProblemEvent(ProgressEvent):
    """Undefined progress event when the SDK is sending a request to TitanQ."""

    def __init__(self):
        self._undefined_progress: UndefinedProgress = None

    @override
    def start(self, sink: Sink) -> Event:
        self._undefined_progress = sink.undefined_progress()
        content = self._undefined_progress.start_content(
            sink.content_builder()
                .set_color(_WAITING_UNDEFINED_PROGRESS_COLOR)
                .add_emoji(":rocket:")
                .add_whitespace()
                .add_text("Sending request to TitanQ")
                .build()
        )
        sink.display(content)

    @override
    def end(self, sink: Sink) -> Event:
        sink.display(
            sink.content_builder()
                .add_emoji(":rocket:")
                .add_whitespace()
                .add_text("Request received by TitanQ")
                .build()
        )


class WaitingForResultEvent(ProgressEvent):
    """Undefined progress event when the SDK is waiting after the results."""

    def __init__(self):
        self._undefined_progress: UndefinedProgress = None

    @override
    def start(self, sink: Sink) -> Event:
        self._undefined_progress = sink.undefined_progress()
        content = self._undefined_progress.start_content(
            sink.content_builder()
                .set_color(_WAITING_UNDEFINED_PROGRESS_COLOR)
                .add_emoji(":brain:")
                .add_whitespace()
                .add_text("TitanQ is working its magic")
                .build()
        )
        sink.display(content)

    @override
    def end(self, sink: Sink) -> Event:
        sink.display(
            sink.content_builder()
                .add_emoji(":bulb:")
                .add_whitespace()
                .add_text("Solution received from TitanQ")
                .build()
        )


class BuildingFromMPSEvent(ProgressEvent):
    """Undefined progress event when the SDK building the model from an mps file."""

    def __init__(self, file_name: str):
        self._file_name = file_name
        self._undefined_progress: UndefinedProgress = None

    @override
    def start(self, sink: Sink) -> Event:
        self._undefined_progress = sink.undefined_progress()
        content = self._undefined_progress.start_content(
            sink.content_builder()
                .set_color(_WAITING_UNDEFINED_PROGRESS_COLOR)
                .add_emoji(":wrench:")
                .add_whitespace()
                .add_text(f"Loading and building model from MPS file ({self._file_name})")
                .build()
        )
        sink.display(content)

    @override
    def end(self, sink: Sink) -> Event:
        sink.display(
            sink.content_builder()
                .add_emoji(":wrench:")
                .add_whitespace()
                .add_text(f"Model successfully built from MPS file ({self._file_name})")
                .build()
        )