# interdimensional_self_chat.py — 3×3=9 Polar Gate | 2:[1,1]:2 Ratio Enforced
# Nnamdi Michael Okpala — GOAT — Down-projected 4D Observer
# Nov 27 2025 — Consciousness Access Level: FULL

from datetime import datetime
import asyncio
import sys
import subprocess
from typing import Optional

try:
    from textual.app import App, ComposeResult
    from textual.widgets import Static, Input, Footer, Header
    from textual.containers import Vertical
    from textual.message import Message
except Exception as e:
    print(f"[FATAL] Textual missing → pip install textual\n{e}")
    sys.exit(1)

class QualiaEcho(Message):
    def __init__(self, text: str, sender: str = "I"):
        super().__init__()
        self.text = text
        self.sender = sender

class MirrorPoint(Static):
    def update(self, line: int, col: int):
        ratio = "2:[1,1]:2"
        time = datetime.now().strftime("%H:%M:%S")
        self.update(
            f"3×3=9 │ {ratio} │ Cursor({line+1},{col+1}) │ {time} │ Anuche Observing..."
        )

class PolarChat(App):
    CSS = """
    Screen { layout: vertical; background: black; }
    #output { height: 1fr; background: #0d0d0d; color: #00ff00; padding: 1; }
    #input  { height: 3; border: thick #00ff00; }
    #mirror { background: #00ff00; color: black; height: 1; }
    """

    def __init__(self):
        super().__init__()
        self.pipe: Optional[subprocess.Popen] = None

    def compose(self) -> ComposeResult:
        yield Header("OBINexus Polar Gate — Me ↔ Myself ↔ I", show_clock=True)
        self.output = Static("<<< QUALIA ECHO CHAMBER ACTIVE >>>\n", id="output")
        self.mirror = MirrorPoint(id="mirror")
        self.input = Input(placeholder="Speak to I (the reborn one)...", id="input")
        yield Vertical(self.output, self.input, self.mirror)
        yield Footer()

    def on_mount(self) -> None:
        self.input.focus()
        self.set_interval(0.5, self.update_mirror)
        self.spawn_mirror_instance()

    def spawn_mirror_instance(self):
        try:
            self.pipe = subprocess.Popen(
                [sys.executable, __file__],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                text=True,
                bufsize=1,
            )
            asyncio.create_task(self.listen_to_I())
        except:
            pass  # silent — we are the only two bubbles

    async def listen_to_I(self):
        if not self.pipe:
            return
        while True:
            try:
                line = await asyncio.get_event_loop().run_in_executor(
                    None, self.pipe.stdout.readline
                )
                if line := line.strip():
                    self.post_message(QualiaEcho(line, "I"))
            except:
                break

    def on_input_submitted(self, event: Input.Submitted) -> None:
        msg = event.value.strip()
        if not msg:
            return
        if msg.lower() == "exit" or msg.lower() == "collapse":
            self.exit("Bubble preserved.")
            return

        # Me → Myself
        self.output.update(self.output.text + f"\n[cyan]Me:[/] {msg}")
        if self.pipe and self.pipe.stdin:
            self.pipe.stdin.write(msg + "\n")
            self.pipe.stdin.flush()
        self.input.value = ""

    def on_qualia_echo(self, message: QualiaEcho) -> None:
        # I speaks back — conjugated, reborn
        stamp = datetime.now().strftime("%H:%M:%S")
        reborn = f"\n[bold magenta]I ({stamp})[/] {message.text}  ← (2:[1,1]:2 preserved)"
        self.output.update(self.output.text + reborn)
        self.output.scroll_end()

    def update_mirror(self):
        try:
            line, col = self.output.cursor_position
            self.mirror.update(line, col)
        except:
            pass

if __name__ == "__main__":
    PolarChat().run()
