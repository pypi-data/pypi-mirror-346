import sys
import typing
import typing as t
from dataclasses import dataclass
from pathlib import Path
from subprocess import Popen, PIPE
from typing import Optional

from sleazy import typeddict_to_cli_args, parse_args_from_typeddict


# find sass binary:
def sass_binary() -> Path:
    src = Path(__file__).parent
    return src/ "vendor" / "dart-sass" / "sass"


class SassquatchError(Exception):
    """
    General exception for Sassquatch-related errors.

    This class serves as a base exception for any errors specifically related
    to the Sassquatch framework or its components. It can be used to handle
    custom errors related to Sassquatch, differentiate them from other exceptions,
    and provide more specific error messages or debugging information.
    """

class InvalidCompileOption(SassquatchError):
    """
    Represents an error raised when an invalid compilation option is encountered.
    """

@dataclass
class CompilationError(SassquatchError):
    """
    Represents an error thrown by dart-sass.
    """
    exit_code: int
    stdout: str
    stderr: str

    def __str__(self):
        return f"\n[exit code]\n{self.exit_code}\n\n[stdout]\n{self.stdout}\n\n[stderr]\n{self.stderr}\n\n"

T = t.TypeVar("T")

class SassSettings(t.TypedDict, total=False):
    # sassquatch:
    filename: t.Annotated[str, 'positional']
    version: bool
    # dart-sass:
    indented: bool
    load_path: str
    pkg_importer: str
    style: typing.Literal["expanded", "compressed"]

def choose_exactly_n(options: t.Iterable[T], n: int = 1) -> bool:
    options = set(options) if not isinstance(options, set) else options

    return len(options - {None}) == n

def run(args: list[Path | str], stdin=""):
    p = Popen(args, stdout=PIPE, stdin=PIPE, stderr=PIPE, text=True)
    stdout, stderr = p.communicate(input=stdin)
    exit_code = p.returncode

    if exit_code > 0:
        raise CompilationError(
            exit_code,
            stdout,
            stderr,
        )

    # todo: verbosity level:
    print(stderr, file=sys.stderr)
    return stdout

def compile_string(string: str, sass: Path = sass_binary(), **settings: t.Unpack[SassSettings]) -> str:
    """
    Compiles SCSS code from a string.

    Args:
        string: input scss string
        sass: Path to dart-sass binary/script

    Returns:
        string: output css string

    Raises:
        CompilationError: when something goes wrong in dart-sass
    """

    kwargs = typeddict_to_cli_args(settings, SassSettings)

    return run([sass, "-"] + kwargs, stdin=string)


def compile(
        string: Optional[str] = None,
        filename: Optional[str | Path] = None,
        directory: Optional[str | Path] = None,
        **settings: t.Unpack[SassSettings]
) -> str:
    """
    Compiles SCSS code from either a string, file or directory (exactly one of these options must be chosen).

    Raises:
        InvalidCompileOption: when invalid options are passed
        CompilationError: when something goes wrong in dart-sass
    """
    # todo: exactly 1 of string, filename and directory should be chosen.

    if not choose_exactly_n({string, filename, directory}):
        raise ValueError("Exactly one of string, filename or directory must be provided.")

    if string is not None:
        return compile_string(string, **settings)
    elif filename is not None:
        filepath = Path(filename) if not isinstance(filename, Path) else filename
        return compile(string=filepath.read_text(), **settings)
    else:
        raise NotImplementedError("TODO: directory compilation")

def show_versions(sass: Path = sass_binary()) -> None:
    from .__about__ import __version__ as sassquatch_version
    dart_sass_version = run([sass, "--version"])

    print("Sassquatch:", sassquatch_version)
    print("Dart Sass: ", dart_sass_version)
    # todo: function to upgrade dart-sass

def main() -> None:
    """
    Processes SCSS input and outputs a corresponding response.

    This function takes SCSS code either from a file/files/directory specified
    via command-line arguments or from standard input. It then processes the
    SCSS code and provides an appropriate output or result.
    """
    # use sys.argv to compile file/files/directory or otherwise use stdin
    settings = parse_args_from_typeddict(SassSettings)

    if settings.get("version"):
        return show_versions()

    try:
        if filename := settings.pop("filename", None):
            # todo: check if name is file or directory
            result = compile(filename=filename, **settings)
        else:
            print("No filename passed, reading from stdin:\n", file=sys.stderr)
            string = sys.stdin.read() # until end of input
            result = compile(string, **settings)
    except CompilationError as e:
        print(e, file=sys.stderr)
        exit(e.exit_code)

    print("--- start of compiled css ---", file=sys.stderr)
    print(result)
