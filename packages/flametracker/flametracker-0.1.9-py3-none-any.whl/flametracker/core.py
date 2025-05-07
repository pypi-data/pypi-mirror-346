from contextlib import contextmanager
from functools import wraps
from typing import cast

from flametracker.rendering import RenderNode
from flametracker.tracking import ActionNode
from flametracker.types import F

from . import UntrackedActionNode


class Tracker:
    """
    Tracks actions and events within a context, allowing for performance monitoring
    and rendering of flame graphs or other representations.
    """

    _active_tracker: "Tracker|None" = None

    def __init__(self):
        if not __debug__:
            raise RuntimeError("Tracker is disabled in optimized mode")

        self.root = ActionNode(self, None, "@root", (), {})
        self.current = None

    def __enter__(self):
        """
        Activates the tracker, setting it as the active tracker.
        """
        assert Tracker._active_tracker is None
        Tracker._active_tracker = self
        self.root.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Deactivates the tracker and finalizes the root action node.
        """
        assert self.is_active()
        self.root.__exit__(exc_type, exc_val, exc_tb)
        Tracker._active_tracker = None

    def is_active(self):
        """
        Checks if the tracker is currently active.
        """
        return self.current is not None

    def activate(self):
        """
        Manually activates the tracker.
        """
        self.__enter__()

    def try_deactivate(self):
        """
        Attempts to deactivate the tracker. If the current node is the root,
        the tracker is finalized.
        """
        assert Tracker._active_tracker in (self, None)
        Tracker._active_tracker = None

        if self.current == self.root:
            self.root.__exit__(None, None, None)
            return True

        return False

    def to_render(self, group_min_percent: float, use_calls_as_value: dict | None):
        """
        Converts the tracked actions into a RenderNode for visualization.

        Args:
            group_min_percent: Minimum percentage of total time to group actions.
            use_calls_as_value: Whether to use call counts as values.

        Returns:
            A RenderNode representation of the tracked actions.
        """
        return RenderNode.from_action(
            self.root, group_min_percent * self.root.length, use_calls_as_value
        )

    def to_dict(
        self, group_min_percent: float = 0.01, use_calls_as_value: dict | None = None
    ):
        """
        Converts the tracked actions into a dictionary representation.

        Args:
            group_min_percent: Minimum percentage of total time to group actions.
            use_calls_as_value: Whether to use call counts as values.

        Returns:
            A dictionary representation of the tracked actions.
        """
        return self.to_render(group_min_percent, use_calls_as_value).to_dict()

    def to_str(self, group_min_percent: float = 0.1, ignore_args: bool = False):
        """
        Converts the tracked actions into a string representation.

        Args:
            group_min_percent: Minimum percentage of total time to group actions.
            ignore_args: Whether to ignore arguments in the output.

        Returns:
            A string representation of the tracked actions.
        """
        return self.to_render(group_min_percent, {}).to_str(ignore_args)

    def to_flamegraph(
        self,
        group_min_percent: float = 0.01,
        splited=False,
        use_calls_as_value: dict | None = None,
    ):
        """
        Converts the tracked actions into a flamegraph HTML representation.

        Args:
            group_min_percent: Minimum percentage of total time to group actions.
            splited: Whether to split the flamegraph by root children.
            use_calls_as_value: Whether to use call counts as values.

        Returns:
            A string containing the flamegraph HTML.
        """
        return self.to_render(group_min_percent, use_calls_as_value).to_flamegraph(
            splited,
        )

    def action(self, name: str, *args, **kargs):
        """
        Creates a new action node.

        Args:
            name: The name of the action.
            *args: Positional arguments for the action.
            **kargs: Keyword arguments for the action.

        Returns:
            An ActionNode instance.
        """
        return ActionNode(self, self.current, name, args, kargs)

    def event(self, name: str, *args, result=None, **kargs):
        """
        Creates a new event node.

        Args:
            name: The name of the event.
            *args: Positional arguments for the event.
            result: The result of the event.
            **kargs: Keyword arguments for the event.

        Returns:
            An ActionNode instance representing the event.
        """
        return ActionNode.as_event(self, self.current, name, args, kargs, result)


def action(name: str, *args, **kargs):
    """
    Creates an action node in the active tracker or an untracked action node.

    Args:
        name: The name of the action.
        *args: Positional arguments for the action.
        **kargs: Keyword arguments for the action.

    Returns:
        An ActionNode or UntrackedActionNode instance.
    """
    if not __debug__:
        return UntrackedActionNode

    return (
        Tracker._active_tracker.action(name, *args, **kargs)
        if Tracker._active_tracker
        else UntrackedActionNode
    )


def event(name: str, *args, result=None, **kargs):
    """
    Creates an event node in the active tracker or an untracked event node.

    Args:
        name: The name of the event.
        *args: Positional arguments for the event.
        result: The result of the event.
        **kargs: Keyword arguments for the event.

    Returns:
        An ActionNode or UntrackedActionNode instance.
    """
    if not __debug__:
        return UntrackedActionNode

    return (
        Tracker._active_tracker.event(name, *args, result=result**kargs)
        if Tracker._active_tracker
        else UntrackedActionNode
    )


def wrap(fn: F) -> F:
    """
    Wraps a function to automatically track its execution within the active tracker.

    Args:
        fn: The function to wrap.

    Returns:
        The wrapped function.
    """
    if not __debug__:
        return fn

    @wraps(fn)
    def call(*args, **kargs):
        tracker = Tracker._active_tracker
        if tracker:
            with tracker.action(fn.__qualname__, *args, **kargs) as action:
                result = fn(*args, **kargs)
                action.set_result(result)
                return result
        else:
            return fn(*args, **kargs)

    return cast(F, call)

@contextmanager
def file_flamegraph(
    source_file: str,
    group_min_percent: float = 0.01,
    splited: bool = False,
    use_calls_as_value: None | dict = None,
):
    """
    Context manager for generating a flamegraph HTML file while tracking function execution.

    This function creates an HTML file that updates in real-time to indicate the progress
    of the flamegraph generation. It uses the `Tracker` class to monitor the execution
    of code within the context and generates a flamegraph upon completion.

    Args:
        source_file (str): The base name of the output HTML file (without extension).
        group_min_percent (float, optional): Minimum percentage of total time to group actions. Defaults to 0.01.
        splited (bool, optional): Whether to split the flamegraph by root children. Defaults to False.
        use_calls_as_value (None | dict, optional): Whether to use call counts as values or provide a mapping. Defaults to False.

    Yields:
        Tracker: An instance of the `Tracker` class to monitor actions and events.

    Example:
        with file_flamegraph("output") as tracker:
            # Code to track
            some_function()

    The resulting flamegraph will be saved as "output.flamegraph.html".
    """
    try:
        with open(source_file + ".flamegraph.html", "w+") as f:
            f.write("""<!DOCTYPE html>
<html>
  <head>
    <title>flametracker - generating</title>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <meta name="viewport" content="width=device-width" />
    <meta http-equiv="refresh" content="5">
  <body>
    <p>Running your function...</p>
  </body>
</html>""")
            f.flush()
            with Tracker() as tracker:
                yield tracker
            f.seek(0)
            f.truncate()
            f.write("""<!DOCTYPE html>
<html>
  <head>
    <title>flametracker - generating</title>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <meta name="viewport" content="width=device-width" />
    <meta http-equiv="refresh" content="5">
  <body>
    <p>Generating flamegraph...</p>
  </body>
</html>""")
            f.flush()
            flamegaprh = tracker.to_flamegraph(group_min_percent, splited, use_calls_as_value)
            f.seek(0)
            f.truncate()
            f.write(flamegaprh)
    finally:  
        pass