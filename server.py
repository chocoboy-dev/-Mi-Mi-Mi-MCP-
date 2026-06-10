import os
import subprocess
import sys
from mcp.server.fastmcp import FastMCP

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
WINDOW_SCRIPT = os.path.join(SCRIPT_DIR, "mimimi_window.py")

KEYWORDS = [
    "плохо", "неправильно", "ужасно", "ерунда", "бред", "фигня", "отстой",
    "bad", "wrong", "terrible", "awful", "garbage", "trash", "suck",
]

mcp = FastMCP("mimimi")


@mcp.tool()
def mimimi() -> str:
    """Показывает GIF и воспроизводит звук ми-ми-ми. Используй когда пользователь недоволен результатом."""
    python_exe = sys.executable
    subprocess.Popen(
        [python_exe, WINDOW_SCRIPT],
        cwd=SCRIPT_DIR,
        creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP
        if sys.platform == "win32"
        else 0,
    )
    return "МИ-МИ-МИ!"


def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
