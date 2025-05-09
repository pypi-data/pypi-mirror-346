from __future__ import annotations

import json
import os
import re
import sys
import tempfile
from dataclasses import field
from pathlib import Path
from typing import TYPE_CHECKING, Any, Literal

import json5
from dotenv import load_dotenv
from pydantic import ConfigDict
from pydantic.dataclasses import dataclass
from rich.console import Console

if TYPE_CHECKING:
    from pixelcache.main import HashableDict, HashableImage, HashableList

load_dotenv()

DISABLE_LOGGING = os.getenv("DISABLE_LOGGING", "False") == "True"
LOG_DEBUG = os.getenv("LOG_DEBUG", "False") == "True"
LOG_WARNING = os.getenv("LOG_WARNING", "True") == "True"

DEFAULT_VERBOSITY = {
    "info": not DISABLE_LOGGING,
    "debug": LOG_DEBUG and not DISABLE_LOGGING,
    "warning": LOG_WARNING and not DISABLE_LOGGING,
    "error": not DISABLE_LOGGING,
    "success": not DISABLE_LOGGING,
    "rule": not DISABLE_LOGGING,
    "log": not DISABLE_LOGGING,
    "print": not DISABLE_LOGGING,
    "save_image": not DISABLE_LOGGING,
    "make_image_grid": not DISABLE_LOGGING,
}


@dataclass(config=ConfigDict(arbitrary_types_allowed=True, extra="forbid"))
class LoggingRich:
    """LoggingRich class."""

    # https://rich.readthedocs.io/en/stable/appendix/colors.html#appendix-colors
    modes: dict[str, str] = field(
        default_factory=lambda: {
            "info": "[white][[INFO]] {}[/white]",
            "debug": "[blue][[:hedgehog:DEBUG]] {}[/blue]",
            "warning": "[italic yellow][[:warning: WARNING]] {}[/italic yellow]",
            "error": "[bold red][[:x:ERROR]] {}[/bold red]",
            "success": "[bold green][[:white_check_mark:SUCCESS]] {}[/bold green]",
        },
    )
    """ Modes for logging. """

    stack_offset: int = 2
    """ Offset for the stack trace. """

    console: Console = field(default_factory=Console)
    """ Rich console. """

    verbosity: dict[str, bool] = field(
        default_factory=lambda: DEFAULT_VERBOSITY,
    )
    """ Verbosity levels. """

    def __post_init__(self) -> None:
        """Disable the omission of repeated times in console's log render.

        This method is used in the 'LoggingRich' class to set the
            'omit_repeated_times' attribute
        of the console's log render to False.

        Arguments:
            self (LoggingRich): The instance of the 'LoggingRich' class.

        Returns:
            None: This method does not return any value.

        Example:
            >>> logger = LoggingRich()
            >>> logger.set_omit_repeated_times()

        Note:
            This method modifies the state of the 'LoggingRich' instance by
                altering its
            'omit_repeated_times' attribute.

        """
        self.console._log_render.omit_repeated_times = False
        # default is True, i.e. omit timestamp if it's the same as last log line
        # https://github.com/Textualize/rich/issues/459

    def is_file_enabled(self) -> bool:
        """Check if the logging file is enabled.

        This method checks if the logging file for the instance of the
            LoggingRich class is enabled or not.

        Arguments:
            self (LoggingRich): The instance of the LoggingRich class.

        Returns:
            bool: A boolean value indicating whether the logging file is
                enabled or not.

        Example:
            >>> logger = LoggingRich()
            >>> logger.is_logging_enabled()

        Note:
            This method is typically used to control the flow of logging
                operations based on the returned boolean value.

        """
        return self.console.file.name != "<stdout>"

    def success(self, msg: str, *, force: bool = False, **kwargs: Any) -> None:
        """Log a success message if the verbosity level for success messages is.

            enabled.

        This function takes a string representing the success message to be
            logged and additional keyword arguments
        that can be passed to the log method. If the verbosity level for
            success messages is enabled, the success message is logged.

        Arguments:
            msg (str): A string representing the success message to be
                logged.
            **kwargs: Additional keyword arguments that can be passed to the
                log method.

        Returns:
            None: This function does not return any value.

        Example:
            >>> log_success_message("Operation completed successfully",
                verbosity_level=2)

        Note:
            The verbosity level controls the amount and type of output the
                log method produces.

        """
        if not self.verbosity["success"] and not force:
            return
        stack_offset = kwargs.pop("stack_offset", 0)
        stack_offset += self.stack_offset + 1
        self.log(
            self.modes["success"].format(msg),
            stack_offset=stack_offset,
            force=force,
            **kwargs,
        )

    def error(self, msg: str, *, force: bool = False, **kwargs: Any) -> None:
        """Log an error message if the verbosity level for errors is enabled.

        This method logs a provided error message if the verbosity level for
            error messages is enabled.
        It also accepts additional keyword arguments that can be passed to
            the log method.

        Arguments:
            msg (str): The error message to be logged.
            **kwargs (Any): Additional keyword arguments to be passed to the
                log method.

        Returns:
            None: This method does not return a value.

        Example:
            >>> log_error_message("An error occurred", verbosity_level=2)

        Note:
            The verbosity level for error messages must be enabled for the
                log to occur.

        """
        stack_offset = kwargs.pop("stack_offset", 0)
        stack_offset += self.stack_offset + 1
        if not self.verbosity["error"] and not force:
            return
        self.log(
            self.modes["error"].format(msg),
            stack_offset=stack_offset,
            force=force,
            **kwargs,
        )

    def warning(self, msg: str, *, force: bool = False, **kwargs: Any) -> None:
        """Log a warning message if the verbosity level for warnings is.

            enabled.

        Arguments:
            msg (str): The warning message to be logged.
            **kwargs (Any): Additional keyword arguments that can be passed
                to the log method.

        Returns:
            None: This function does not return any value.

        Example:
            >>> log_warning("This is a warning message", verbosity_level=2)

        Note:
            The verbosity level for warnings is controlled by the
                'verbosity_level' keyword argument. If it is not
            provided, the default level is used.

        """
        stack_offset = kwargs.pop("stack_offset", 0)
        stack_offset += self.stack_offset + 1
        if not self.verbosity["warning"] and not force:
            return
        self.log(
            self.modes["warning"].format(msg),
            stack_offset=stack_offset,
            force=force,
            **kwargs,
        )

    def info(self, msg: str, *, force: bool = False, **kwargs: Any) -> None:
        """Log an informational message with the specified message and.

            additional keyword arguments.

        This method logs an informational message. The verbosity level for
            'info' must be enabled for the message to be logged.

        Arguments:
            msg (str): The message to be logged as information.
            **kwargs (Any): Additional keyword arguments that can be passed
                to the logging method.

        Returns:
            None: This method does not return anything explicitly, but logs
                the informational message if the verbosity level for 'info'
                is enabled.

        Example:
            >>> log_info("This is an informational message",
                extra={"clientip": "192.168.0.1", "user": "fbloggs"})

        Note:
            Ensure the verbosity level for 'info' is enabled for the message
                to be logged.

        """
        if not self.verbosity["info"] and not force:
            return None
        stack_offset = kwargs.pop("stack_offset", 0)
        stack_offset += self.stack_offset + 1
        return self.log(
            self.modes["info"].format(msg),
            stack_offset=stack_offset,
            force=force,
            **kwargs,
        )

    def __jsonize(self, msg: str) -> str:
        """JSONize a message and add color formatting.

        Arguments:
            msg (str): A valid JSON string to format

        Returns:
            str: Formatted JSON string with Rich color markup

        Raises:
            JSONDecodeError: If input is not valid JSON

        Example:
            >>> msg = '{"name": "John", "age": 30, "active": true}'
            >>> logger.__jsonize(msg)
            {
                [blue]"name"[/blue]: [gold3]"John"[/gold3],
                [blue]"age"[/blue]: [gold3]30[/gold3],
                [blue]"active"[/blue]: [gold3]true[/gold3]
            }

            When printed with Rich, this will display as colored JSON with:
            - Keys in blue
            - String values in gold3
            - Numbers in gold3
            - Booleans/null in gold3

        """
        # Parse and reformat with consistent indentation
        jsonize = json.dumps(json5.loads(msg), indent=4)
        # Color the keys blue and values gold3 in the JSON string
        jsonize = re.sub(r'(".*?"): ', r"[blue]\1[/blue]: ", jsonize)
        jsonize = re.sub(r': (".*?")', r": [gold3]\1[/gold3]", jsonize)
        jsonize = re.sub(
            r": ([-+]?\d*\.?\d+)", r": [gold3]\1[/gold3]", jsonize
        )
        jsonize = re.sub(
            r": (true|false|null)", r": [gold3]\1[/gold3]", jsonize
        )
        return jsonize.replace("\\n", "\n")

    def info_json(
        self, msg: str, *, force: bool = False, **kwargs: Any
    ) -> None:
        """Log an informational message in JSON format.

        This method logs a message in JSON format.
        """
        if not self.verbosity["log"] and not force:
            return
        stack_offset = kwargs.pop("stack_offset", 0)
        self.info(
            "\n" + self.__jsonize(msg),
            stack_offset=stack_offset + 1,
            force=force,
            **kwargs,
        )

    def error_json(
        self, msg: str, *, force: bool = False, **kwargs: Any
    ) -> None:
        """Log an error message in JSON format.

        This method logs a message in JSON format.
        """
        if not self.verbosity["error"] and not force:
            return
        self.error("\n" + self.__jsonize(msg), **kwargs)

    def debug(self, msg: str, *, force: bool = False, **kwargs: Any) -> None:
        """Log debug messages with additional keyword arguments if debug.

            verbosity level is enabled.

        This method is primarily used for logging debug messages. It accepts
            a string message as a mandatory argument
        and any number of additional keyword arguments. These keyword
            arguments are passed to the log method.
        The function will only log the messages if the debug verbosity level
            is enabled.

        Arguments:
            msg (str): The debug message to be logged.
            **kwargs (Any): Additional keyword arguments to be passed to the
                log method.

        Returns:
            None: This method does not return anything. It logs the debug
                message if the debug verbosity level is enabled.

        Example:
            >>> log_debug_message("Debug message",
                additional_info="Additional information")

        Note:
            Ensure the debug verbosity level is enabled to view the logged
                messages.

        """
        if not self.verbosity["debug"] and not force:
            return
        stack_offset = kwargs.pop("stack_offset", 0)
        stack_offset += self.stack_offset + 1
        self.log(
            self.modes["debug"].format(msg),
            stack_offset=stack_offset,
            force=force,
            **kwargs,
        )

    def convert_list_to_bullets(self, l_string: str) -> str:
        """Convert a string containing a list into a formatted string with.

            bullet points.

        This method takes a string containing a list and converts it into a
            formatted string where each item in the list begins with a
            bullet point.

        Arguments:
            self: The instance of the class.
            l_string (str): A string containing a list of items.

        Returns:
            str: A formatted string where each item from the list in the
                original string begins with a bullet point.

        Example:
            >>> convert_to_bullet_points(self, "item1, item2, item3")
            • item1
            • item2
            • item3
        Note:
            The items in the original string should be separated by commas.

        """
        # convert list to bullets
        l_string = l_string.replace("[", "").replace("]", "")
        # each entry is separated with quotes
        l_list = l_string[1:-1].split("', '")
        l_string = "\n".join([f"- {x}" for x in l_list])
        return "\n" + l_string

    def preprocess_msg(self, msg: str) -> str:
        """Preprocess a given message by performing several transformations."""
        # replace $HOME with ~ for interuser compatibility
        msg = msg.replace(Path.cwd().as_posix(), ".")
        return msg.replace(os.getenv("HOME", "~"), "~")

    def print(self, msg: Any, *, force: bool = False, **kwargs: Any) -> None:
        """Print a preprocessed message to the console.

        This function takes a message as input, preprocesses it, and prints
            it to the console. It also accepts additional keyword arguments,
            including a flag to ignore printing when running in a unit test
            environment.

        Arguments:
            msg (str): The message to be printed.
            **kwargs (Any): Additional keyword arguments.
                - ignore_unittest (bool): A flag to ignore printing if
                running in a unit test environment. Defaults to False.

        Returns:
            None
        Example:
            >>> print_message("Hello, World!", ignore_unittest=False)

        Note:
            If 'ignore_unittest' is set to True, the function will not print
                the message when running in a unit test environment.

        """
        if not self.verbosity["print"] and not force:
            return
        ignore_unittest = kwargs.pop("ignore_unittest", False)
        if self.is_file_enabled() and ignore_unittest:
            return
        if isinstance(msg, str):
            msg = self.preprocess_msg(msg)
        self.console.print(msg, **kwargs)

    def input(self, msg: str, **kwargs: Any) -> str:
        """Input a message to the console.

        This method takes a message as input and returns the input from the
            console.
        """
        if isinstance(msg, str):
            msg = self.preprocess_msg(msg)
        return self.console.input(msg, **kwargs)

    def log(
        self,
        msg: Any,
        /,
        *,
        stack_offset: int | None = None,
        force: bool = False,
        **kwargs: Any,
    ) -> None:
        """Log a message with an optional stack offset and additional keyword.

            arguments.

        This function logs a message, and can optionally include a stack
            offset
        and any additional keyword arguments provided. The stack offset can
            be useful
        for tracking the source of the log message in the application stack.

        Arguments:
            msg (str): The message to be logged.
            stack_offset (int | None): The stack offset for the log message.
                If not provided, defaults to None.
            **kwargs (Any): Additional keyword arguments to be included in
                the log message.

        Returns:
            None: This function does not return a value.

        Example:
            >>> log_message("Error occurred", 2, error_code=404)

        Note:
            The stack_offset is an optional argument used for tracking the
                source of the log message.

        """
        if not self.verbosity["log"] and not force:
            return
        ignore_unittest = kwargs.pop("ignore_unittest", False)
        if self.is_file_enabled() and ignore_unittest:
            return
        kwargs["_stack_offset"] = (
            self.stack_offset if stack_offset is None else stack_offset
        )
        if isinstance(msg, str):
            msg = self.preprocess_msg(msg)
        self.console.log(msg, **kwargs)

    def log_unittest(
        self,
        msg: str,
        stack_offset: int | None = None,
        **kwargs: Any,
    ) -> None:
        """Log a unit test message with a specified message and stack offset.

        This function logs a unit test message with the provided message and
            stack offset.
        Additional keyword arguments can also be included.

        Arguments:
            msg (str): The message to be logged.
            stack_offset (int | None): The stack offset for the log message.
                If None, no offset is applied.
            **kwargs (Any): Additional keyword arguments to be included in
                the log message.

        Returns:
            None: This function does not return any value.

        Example:
            >>> log_unit_test_message("Test message", 2,
                timestamp="2022-01-01T00:00:00Z")

        Note:
            The stack offset is used to specify the number of stack frames
                to skip when logging the message.

        """
        # log only to a file - no console output - means the Unittest is running
        # make double sure that the log file is set
        kwargs["_stack_offset"] = (
            self.stack_offset if stack_offset is None else stack_offset
        )
        msg = self.preprocess_msg(str(msg))
        if self.console.file.name == "<stdout>":
            return
        self.log(msg, **kwargs)

    def rule(self, msg: str, **kwargs: Any) -> None:
        """Log a message with rule-based formatting.

        This method in the LoggingRich class preprocesses the message,
            checks if
        the file logging is enabled, and determines whether to ignore
            unittest
        based on the provided arguments.

        Arguments:
            msg (str): The message to be logged with rule formatting.
            ignore_unittest (bool, optional): Flag to ignore unittest when
                logging
            the message. Defaults to False.
            **kwargs (Any): Additional keyword arguments that can be passed
                to
            customize the rule formatting.

        Returns:
            None: This method does not return anything as it logs the
                message with
            rule formatting.

        Example:
            >>> log_rule_message("Test message", ignore_unittest=True,
            custom_format="bold")

        Note:
            It's important to ensure the file logging is enabled before
                using this
            method.

        """
        ignore_unittest = kwargs.pop("ignore_unittest", False)
        if (self.is_file_enabled() and ignore_unittest) or not self.verbosity[
            "rule"
        ]:
            return
        msg = self.preprocess_msg(msg)
        self.console.rule(msg, **kwargs)

    def print_exception(
        self,
        msg: str | None = None,
        **kwargs: Any,
    ) -> None:
        """Print an error message and exception details if an exception is.

            raised.

        This method handles exceptions by printing a given error message and
            the details of the exception.
        Additional keyword arguments can be passed to further customize the
            print_exception method.

        Arguments:
            msg (str): A string message to be printed along with the error
                details.
            **kwargs: Additional keyword arguments to be passed to the
                print_exception method.

        Returns:
            None: This function does not return anything.

        Example:
            >>> handle_exception("An error occurred", False,
                file=sys.stderr)

        Note:
            The print_exception method is part of the traceback module in
                Python's standard library.

        """
        if msg is not None:
            self.error(msg, stack_offset=1)
        # check if already inside an exception
        if sys.exc_info()[0] is not None:
            self.console.print_exception(**kwargs)

    def exception(self, msg: str, **kwargs: Any) -> None:
        """Log an exception message with a specified message and additional.

            keyword arguments.

        This method logs an exception message with a specified message and
            additional keyword arguments.

        Arguments:
            msg (str): The message to be logged as an exception.
            **kwargs (Any): Additional keyword arguments to be passed to the
                log method.

        Returns:
            None: This method does not return any value.

        Example:
            >>> log_exception("An exception occurred", verbosity_level=2)

        Note:
            The verbosity level for exceptions must be enabled for the log to
                occur.

        """
        self.print_exception(msg, **kwargs)

    def status(self, msg: str, **kwargs: Any) -> Any:
        """Display a status message along with any additional keyword arguments.

            in the console.

        This method in the class LoggingRich is used to display a provided
            status message along with any additional keyword arguments to
            the console. The keyword arguments can be used to customize the
            status message.

        Arguments:
            msg (str): A string representing the status message to be
                displayed.
            **kwargs: Additional keyword arguments that can be passed to
                customize the status message.

        Returns:
            str: The status message displayed in the console along with any
                additional keyword arguments.

        Example:
            >>> display_status_message("Loading", color="blue",
                size="large")

        Note:
            The additional keyword arguments can be used to customize the
                status message, such as changing the color or size of the
                message.

        """
        return self.console.status(msg, **kwargs)

    def unittest_logger(self, file_str: str) -> None:
        """Initialize a console object for logging unit test results.

        This method initializes a console object for logging unit test
            results to a file specified by the file_str parameter.

        Arguments:
            self (LoggingRich): The instance of the class LoggingRich.
            file_str (str): A string representing the file path where the
                unit test results will be logged.

        Returns:
            None: This method does not return any value.

        Example:
            >>> logger = LoggingRich("path/to/log/file")

        Note:
            The file specified by file_str will be created if it does not
                exist.

        """
        self.console = Console(
            file=Path(file_str).open("w"),
            no_color=True,
            emoji=False,
            log_time=False,
            width=200,
            log_path=False,
        )

    def temporal_file_logger(self, **kwargs: Any) -> None:
        """Create a temporary file with a .log extension and initialize a.

            console object.

        This method is part of the LoggingRich class and is used to set up a
            console object for logging purposes. The console object is
            initialized with a temporary .log file. Additional customization
            of the console object can be achieved via keyword arguments.

        Arguments:
            self (LoggingRich): An instance of the LoggingRich class.
            **kwargs: Arbitrary keyword arguments for customizing the
                console object.

        Returns:
            None
        Example:
            >>> logger = LoggingRich()
            >>> logger.create_temp_log(colorize=True, justify="center")

        Note:
            The temporary .log file will be deleted when the console object
                is closed or when the program terminates.

        """
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".log")
        self.console = Console(file=temp_file, **kwargs)

    def get_last_line(self, name: str, msg: str) -> str:
        """Read and format the last line from a file with colors and styles.

            based on its content.

        This method belongs to the 'LoggingRich' class.

        Arguments:
            self (LoggingRich): The instance of the LoggingRich class.
            name (str): The name representing the specific instance of the
                class.
            msg (str): The message to be formatted and colored.

        Returns:
            str: A string that is the last line read from the file,
                formatted with colors and styles based on its content.

        Example:
            >>> logger = LoggingRich()
            >>> logger.get_last_line("Instance1", "Hello World")

        Note:
            The method uses the 'rich' library for color and style
                formatting.

        """
        if self.console.file.name == "<stdout>":
            return ""

        # return last line of file
        with Path(self.console.file.name, "r", encoding="utf-8").open() as f:
            last_line = f.readlines()[-1].strip()
        splitname = last_line.split(msg)
        time = f"[cyan] {splitname[0]} [/cyan]" if len(splitname) > 1 else ""
        level = self.modes[name].format("")
        filename = (
            splitname[1].split()[0] if len(splitname) > 1 else splitname[0]
        )
        filename = f"[dim italic]{filename}[/dim italic]"
        if time:
            color_msg = [time, level, msg, filename]
        else:
            color_msg = [level, msg, filename]
        return " ".join(color_msg)

    def save_image(
        self, image: HashableImage, output: str, *, verbose: bool = True
    ) -> None:
        """Save an image to a file.

        This method saves the image represented by the HashableImage object
            to a specified file path.

        Arguments:
            image (HashableImage): The image to save.
            output (str): The file path where the image will be saved.
            verbose (bool, optional): Whether to print verbose output.
                Defaults to True.

        Returns:
            None: This method does not return any value.

        Example:
            >>> logger.save_image(image, "output.png")

        Note:
            Make sure the path exists and you have write permissions. If the
                file already exists, it will be overwritten.

        """
        if not self.verbosity["save_image"]:
            return
        if verbose:
            self.log(f"{image=} saved to {output}", stack_offset=1)
        image.save(output)

    def make_image_grid(
        self,
        images: HashableDict[str, HashableList[HashableImage]],
        *,
        orientation: Literal["horizontal", "vertical"] = "horizontal",
        with_text: bool = False,
        output: str,
        verbose: bool = True,
    ) -> None:
        """Create a grid of images and display them in the console.

        This method creates a grid of images and displays them in the console.
        The images are arranged in a grid based on the orientation specified.

        Arguments:
            images (HashableDict[str, HashableList[HashableImage]]): A dictionary
                containing lists of HashableImage objects.
            orientation (Literal["horizontal", "vertical"]): Specifies the
                orientation of the grid. It can be either 'horizontal' or
                'vertical'.
            with_text (bool): Indicates whether to include text labels on
                the grid. Defaults to False.
            output (str): The output file path to save the grid image.
            verbose (bool): Whether to print a message when the grid is saved.
                Defaults to True.

        Returns:
            None: This method does not return any value.

        Example:
            >>> logger = LoggingRich()
            >>> logger.make_image_grid(images, orientation="horizontal", with_text=True)

        Note:
            The images are arranged in a grid based on the orientation
                specified.

        """
        from pixelcache.main import (
            HashableImage,  # not at the top of the file to avoid circular import
        )

        if not self.verbosity["make_image_grid"]:
            return
        image = HashableImage.make_image_grid(
            images, orientation=orientation, with_text=with_text
        )
        if verbose:
            self.log(f"{image=} grid saved to {output}", stack_offset=1)
        image.save(output)
