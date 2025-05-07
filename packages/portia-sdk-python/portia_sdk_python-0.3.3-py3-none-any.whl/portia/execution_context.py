"""Provides execution context to the planning and execution agents.

This module defines the `ExecutionContext` class and utilities for managing execution
contexts for planning and execution agents. It provides a way to pass runtime-specific information
for each run execution, ensuring flexibility and context isolation, especially in
multi-threaded or asynchronous applications.

Key Features:
- The `ExecutionContext` class encapsulates information such as user identification
  and additional data for planning and execution agents.
- The `execution_context` context manager allows for context isolation, ensuring
  that each task or thread has its own independent execution context.
- The `get_execution_context` function allows retrieval of the current execution context.

"""

from __future__ import annotations

from contextlib import contextmanager
from contextvars import ContextVar
from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field

if TYPE_CHECKING:
    from collections.abc import Generator

# Define a ContextVar for execution context
_execution_context: ContextVar[ExecutionContext | None] = ContextVar(
    "_execution_context",
    default=None,
)


class ExecutionContext(BaseModel):
    """Execution context provides runtime information to the portia client and planning and execution agents.

    Unlike configuration settings, it is designed to be used on a per-request basis,
    allowing customization at runtime. For example, this can pass end-user-specific
    information to planning and execution agents for dynamic adjustments.

    Attributes:
        additional_data (dict[str, str]): Arbitrary additional data useful for debugging.

    """  # noqa: E501

    model_config = ConfigDict(extra="ignore")

    additional_data: dict[str, str] = Field(default={})


def empty_context() -> ExecutionContext:
    """Return an empty execution context.

    Returns:
        ExecutionContext: A default `ExecutionContext` instance with no specific data set.

    """
    return ExecutionContext(
        additional_data={},
    )


@contextmanager
def execution_context(
    context: ExecutionContext | None = None,
    additional_data: dict[str, str] | None = None,
) -> Generator[None, None, None]:
    """Set the execution context for the duration of the PlanRun.

    This context manager ensures context isolation by using `contextvars.ContextVar`,
    meaning that the execution context set within this block will only affect
    the current task or thread. This is particularly useful in both multi-threaded
    and asynchronous applications, such as web servers or task queues, where multiple
    tasks or threads may need independent contexts simultaneously.

    Args:
        context (Optional[ExecutionContext]): The execution context to set for the current task.
            If not provided, a new `ExecutionContext` is created using the provided parameters.
        additional_data (Optional[Dict[str, str]]): Arbitrary additional data to associate
            with the context. Defaults to an empty dictionary.

    Yields:
        None: The block of code within the context manager executes with the specified context.

    Context Isolation:
        - The `_execution_context` object is a `ContextVar`, ensuring that the `ExecutionContext`
          set in one task or thread does not affect others.
        - When the context manager exits, the context for the current task is cleaned up
          to avoid memory leaks or unintended persistence of data.

    Example:
    ```python
        with execution_context(additional_data={"key": "value"}):
            # Code here runs with the specified execution context
        # Outside the block, the execution context is cleared for the current task.
    ```

    """
    if context is None:
        context = ExecutionContext(
            additional_data=additional_data or {},
        )
    token = _execution_context.set(context)
    try:
        yield
    finally:
        _execution_context.reset(token)


def get_execution_context() -> ExecutionContext:
    """Retrieve the current execution context.

    This function retrieves the `ExecutionContext` that is currently set. If no context
    is set, an empty `ExecutionContext` is returned.

    Returns:
        ExecutionContext: The current execution context, or an empty context if none is set.

    """
    return _execution_context.get() or empty_context()


def is_execution_context_set() -> bool:
    """Check whether an execution context is currently set.

    Returns:
        bool: `True` if an execution context is set, otherwise `False`.

    """
    return _execution_context.get() is not None
