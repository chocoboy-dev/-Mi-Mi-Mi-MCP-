import os
import subprocess
import sys
from mcp.server.fastmcp import FastMCP

from triggers import TRIGGERS, ALL_KEYWORDS_RU, ALL_KEYWORDS_EN, find_best_reaction

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
WINDOW_SCRIPT = os.path.join(SCRIPT_DIR, "mimimi_window.py")

mcp = FastMCP("mimimi")


def _launch_window(reaction: str, text: str = ""):
    python_exe = sys.executable
    subprocess.Popen(
        [python_exe, WINDOW_SCRIPT, "--reaction", reaction, "--text", text],
        cwd=SCRIPT_DIR,
        creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP
        if sys.platform == "win32"
        else 0,
    )


def _make_reaction_tool(reaction: str):
    data = TRIGGERS[reaction]
    fn_name = reaction

    def tool(text: str = "") -> str:
        _launch_window(reaction, text)
        return f"{data['emoji']} {data['label']}!"

    tool.__name__ = fn_name
    tool.__doc__ = (
        f"{data['emoji']} {data['label']} — {data['desc']}. "
        f"Используй когда пользователь {data['desc'].lower()}."
    )
    return tool


for reaction in TRIGGERS:
    fn = _make_reaction_tool(reaction)
    mcp.add_tool(fn)


@mcp.tool()
def auto(text: str = "") -> str:
    """Автоматически определяет реакцию по тексту пользователя. Используй когда непонятно какую реакцию выбрать."""
    reaction = find_best_reaction(text)
    if not reaction:
        return auto.__doc__
    _launch_window(reaction, text)
    return f"{TRIGGERS[reaction]['emoji']} {TRIGGERS[reaction]['label']}!"


@mcp.prompt()
def mimimi_keywords() -> str:
    """Системный промпт: список триггер-слов для opencode."""
    ru_sample = ALL_KEYWORDS_RU[:30]
    en_sample = ALL_KEYWORDS_EN[:30]
    return (
        "Ты — Mi-Mi-Mi MCP-сервер. Когда пользователь выражает эмоции по поводу кода, "
        "вызывай соответствующий инструмент реакции:\n\n"
        "Доступные реакции:\n"
        + "\n".join(
            f"  {d['emoji']} `{k}` — {d['label']} ({d['desc']})"
            for k, d in TRIGGERS.items()
        )
        + f"\n\nПримеры триггер-слов (русские): {', '.join(ru_sample)}..."
        + f"\nПримеры триггер-слов (английские): {', '.join(en_sample)}..."
        + "\n\nЕсли не уверен — используй `auto()` с текстом пользователя."
    )


def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
