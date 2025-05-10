from pylsp import hookimpl
import subprocess
import sys


def ruff_format(code: str) -> str:
    return subprocess.check_output(
        [
            sys.executable,
            "-m",
            "ruff",
            "format",
            "-",
        ],
        input=code,
        text=True,
    ).strip()


def wrap_signature(signature: str) -> str:
    as_func = f"def {signature.strip()}:\n    pass"
    try:
        signature = (
            ruff_format(as_func).removeprefix("def ").removesuffix(":\n    pass")
        )
    except subprocess.CalledProcessError:
        pass
    return "```python\n" + signature + "\n```\n"


@hookimpl
def pylsp_signatures_to_markdown(signatures: list[str]) -> str:
    return wrap_signature("\n".join(signatures))
