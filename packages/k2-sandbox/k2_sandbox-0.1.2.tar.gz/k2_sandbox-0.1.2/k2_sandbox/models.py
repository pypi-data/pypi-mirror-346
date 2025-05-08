"""Data models for the K2 Sandbox SDK."""

from dataclasses import dataclass, field
from datetime import datetime
import json
from typing import (
    Any,
    Awaitable,
    Callable,
    Dict,
    Iterable,
    List,
    Optional,
    TypeVar,
    Union,
)
import base64
from k2_sandbox.charts import Chart, _deserialize_chart
import logging

logger = logging.getLogger(__name__)


@dataclass
class Logs:
    """Represents stdout and stderr logs from code execution."""

    stdout: List[Dict[str, Union[str, bool, float]]]
    stderr: List[Dict[str, Union[str, bool, float]]]


@dataclass
class Error:
    """Represents an error from code execution."""

    name: str
    value: str
    traceback: Optional[List[str]] = None


@dataclass
class Result:
    """
    Represents the data to be displayed as a result of executing a cell in a Jupyter notebook.
    The result is similar to the structure returned by ipython kernel: https://ipython.readthedocs.io/en/stable/development/execution.html#execution-semantics

    The result can contain multiple types of data, such as text, images, plots, etc. Each type of data is represented
    as a string, and the result can contain multiple types of data. The display calls don't have to have text representation,
    for the actual result the representation is always present for the result, the other representations are always optional.
    """

    def __getitem__(self, item):
        return getattr(self, item)

    text: Optional[str] = None
    html: Optional[str] = None
    markdown: Optional[str] = None
    svg: Optional[str] = None
    png: Optional[str] = None
    jpeg: Optional[str] = None
    pdf: Optional[str] = None
    latex: Optional[str] = None
    json: Optional[dict] = None
    javascript: Optional[str] = None
    data: Optional[dict] = None
    chart: Optional[Chart] = None
    is_main_result: bool = False
    """Whether this data is the result of the cell. Data can be produced by display calls of which can be multiple in a cell."""
    extra: Optional[dict] = None
    """Extra data that can be included. Not part of the standard types."""

    def __init__(
        self,
        text: Optional[str] = None,
        html: Optional[str] = None,
        markdown: Optional[str] = None,
        svg: Optional[str] = None,
        png: Optional[str] = None,
        jpeg: Optional[str] = None,
        pdf: Optional[str] = None,
        latex: Optional[str] = None,
        json: Optional[dict] = None,
        javascript: Optional[str] = None,
        data: Optional[dict] = None,
        chart: Optional[dict] = None,
        is_main_result: bool = False,
        extra: Optional[dict] = None,
        **kwargs,  # Allows for future expansion
    ):
        self.text = text
        self.html = html
        self.markdown = markdown
        self.svg = svg
        self.png = png
        self.jpeg = jpeg
        self.pdf = pdf
        self.latex = latex
        self.json = json
        self.javascript = javascript
        self.data = data
        if chart:
            try:
                self.chart = _deserialize_chart(chart)
            except Exception as e:
                logger.error(
                    f"Error deserializing chart, check if you are using the latest version of the library: {e}"
                )
        self.is_main_result = is_main_result
        self.extra = extra

    def formats(self) -> Iterable[str]:
        """
        Returns all available formats of the result.

        :return: All available formats of the result in MIME types.
        """
        formats = []
        if self.text:
            formats.append("text")
        if self.html:
            formats.append("html")
        if self.markdown:
            formats.append("markdown")
        if self.svg:
            formats.append("svg")
        if self.png:
            formats.append("png")
        if self.jpeg:
            formats.append("jpeg")
        if self.pdf:
            formats.append("pdf")
        if self.latex:
            formats.append("latex")
        if self.json:
            formats.append("json")
        if self.javascript:
            formats.append("javascript")
        if self.data:
            formats.append("data")
        if self.chart:
            formats.append("chart")

        if self.extra:
            for key in self.extra:
                formats.append(key)

        return formats

    def __str__(self) -> Optional[str]:
        """
        Returns the text representation of the data.

        :return: The text representation of the data.
        """
        return self.__repr__()

    def __repr__(self) -> str:
        if self.text:
            return f"Result({self.text})"
        else:
            return "Result(Formats: " + ", ".join(self.formats()) + ")"

    def _repr_html_(self) -> Optional[str]:
        """
        Returns the HTML representation of the data.

        :return: The HTML representation of the data.
        """
        return self.html

    def _repr_markdown_(self) -> Optional[str]:
        """
        Returns the Markdown representation of the data.

        :return: The Markdown representation of the data.
        """
        return self.markdown

    def _repr_svg_(self) -> Optional[str]:
        """
        Returns the SVG representation of the data.

        :return: The SVG representation of the data.
        """
        return self.svg

    def _repr_png_(self) -> Optional[str]:
        """
        Returns the base64 representation of the PNG data.

        :return: The base64 representation of the PNG data.
        """
        return self.png

    def _repr_jpeg_(self) -> Optional[str]:
        """
        Returns the base64 representation of the JPEG data.

        :return: The base64 representation of the JPEG data.
        """
        return self.jpeg

    def _repr_pdf_(self) -> Optional[str]:
        """
        Returns the PDF representation of the data.

        :return: The PDF representation of the data.
        """
        return self.pdf

    def _repr_latex_(self) -> Optional[str]:
        """
        Returns the LaTeX representation of the data.

        :return: The LaTeX representation of the data.
        """
        return self.latex

    def _repr_json_(self) -> Optional[dict]:
        """
        Returns the JSON representation of the data.

        :return: The JSON representation of the data.
        """
        return self.json

    def _repr_javascript_(self) -> Optional[str]:
        """
        Returns the JavaScript representation of the data.

        :return: The JavaScript representation of the data.
        """
        return self.javascript


@dataclass
class ExecutionError:
    """
    Represents an error that occurred during the execution of a cell.
    The error contains the name of the error, the value of the error, and the traceback.
    """

    name: str
    """
    Name of the error.
    """
    value: str
    """
    Value of the error.
    """
    traceback: str
    """
    The raw traceback of the error.
    """

    def __init__(self, name: str, value: str, traceback: str, **kwargs):
        self.name = name
        self.value = value
        self.traceback = traceback

    def to_json(self) -> str:
        """
        Returns the JSON representation of the Error object.
        """
        data = {"name": self.name, "value": self.value, "traceback": self.traceback}
        return json.dumps(data)


def serialize_results(results: List[Result]) -> List[Dict[str, str]]:
    """
    Serializes the results to JSON.
    """
    serialized = []
    for result in results:
        serialized_dict = {}
        for key in result.formats():
            if key == "chart":
                serialized_dict[key] = result.chart.to_dict()
            else:
                serialized_dict[key] = result[key]

        serialized_dict["text"] = result.text
        serialized.append(serialized_dict)

    return serialized


@dataclass(repr=False)
class Execution:
    """
    Represents the result of a cell execution.
    """

    results: List[Result] = field(default_factory=list)
    """List of the result of the cell (interactively interpreted last line), display calls (e.g. matplotlib plots)."""
    logs: Logs = field(default_factory=Logs)
    """Logs printed to stdout and stderr during execution."""
    error: Optional[ExecutionError] = None
    """Error object if an error occurred, None otherwise."""
    execution_count: Optional[int] = None
    """Execution count of the cell."""

    def __init__(
        self,
        results: List[Result] = None,
        logs: Logs = None,
        error: Optional[ExecutionError] = None,
        execution_count: Optional[int] = None,
        **kwargs,
    ):
        self.results = results or []
        self.logs = logs or Logs()
        self.error = error
        self.execution_count = execution_count

    def __repr__(self):
        return f"Execution(Results: {self.results}, Logs: {self.logs}, Error: {self.error})"

    @property
    def text(self) -> Optional[str]:
        """
        Returns the text representation of the result.

        :return: The text representation of the result.
        """
        for d in self.results:
            if d.is_main_result:
                return d.text

    def to_json(self) -> str:
        """
        Returns the JSON representation of the Execution object.
        """
        data = {
            "results": serialize_results(self.results),
            "logs": self.logs.to_json(),
            "error": self.error.to_json() if self.error else None,
        }
        return json.dumps(data)


@dataclass
class FileInfo:
    """Information about a file or directory in the sandbox."""

    name: str
    is_dir: bool
    size: Optional[int] = None
    path: Optional[str] = None


@dataclass
class ProcessExecution:
    """Result of a process execution."""

    stdout: str
    stderr: str
    exit_code: int


@dataclass
class ProcessInfo:
    """Information about a running process in the sandbox."""

    pid: int
    cmd: str
    user: Optional[str] = None
    cwd: Optional[str] = None
    envs: Optional[Dict[str, str]] = None


@dataclass
class WatchHandle:
    """Handle for watching a directory for filesystem events."""

    id: str
    path: str

    def stop(self):
        """Stop watching the directory."""
        pass


@dataclass
class ProcessHandle:
    """Handle for a running process in the sandbox."""

    pid: int
    cmd: str

    def wait(self) -> ProcessExecution:
        """Wait for the process to complete and return its output."""
        pass

    def send_stdin(self, data: str):
        """Send data to the process stdin."""
        pass

    def kill(self) -> bool:
        """Kill the process."""
        pass


@dataclass
class PtyHandle:
    """Handle for a PTY session in the sandbox."""

    pid: int

    def send_data(self, data: bytes):
        """Send data to the PTY."""
        pass

    def resize(self, rows: int, cols: int):
        """Resize the PTY."""
        pass

    def kill(self) -> bool:
        """Kill the PTY session."""
        pass


@dataclass
class FilesystemEvent:
    """Represents a filesystem event."""

    event_type: str  # "create", "delete", "modify"
    path: str
    is_dir: bool
    timestamp: float


T = TypeVar("T")
OutputHandler = Union[
    Callable[[T], Any],
    Callable[[T], Awaitable[Any]],
]


@dataclass
class OutputMessage:
    """
    Represents an output message from the sandbox code execution.
    """

    line: str
    """
    The output line.
    """
    timestamp: int
    """
    Unix epoch in nanoseconds
    """
    error: bool = False
    """
    Whether the output is an error.
    """

    def __str__(self):
        return self.line


def parse_output(
    execution: Execution,
    output: str,
    on_stdout: Optional[OutputHandler[OutputMessage]] = None,
    on_stderr: Optional[OutputHandler[OutputMessage]] = None,
    on_result: Optional[OutputHandler[Result]] = None,
    on_error: Optional[OutputHandler[ExecutionError]] = None,
):
    data = json.loads(output)
    data_type = data.pop("type")

    if data_type == "result":
        result = Result(**data)
        execution.results.append(result)
        if on_result:
            on_result(result)
    elif data_type == "stdout":
        execution.logs.stdout.append(data["text"])
        if on_stdout:
            on_stdout(OutputMessage(data["text"], data["timestamp"], False))
    elif data_type == "stderr":
        execution.logs.stderr.append(data["text"])
        if on_stderr:
            on_stderr(OutputMessage(data["text"], data["timestamp"], True))
    elif data_type == "error":
        execution.error = ExecutionError(data["name"], data["value"], data["traceback"])
        if on_error:
            on_error(execution.error)
    elif data_type == "number_of_executions":
        execution.execution_count = data["execution_count"]
