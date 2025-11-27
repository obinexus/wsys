# interdimensional_chat_tui.py — 3×3=9 Self-Chat Lensing Terminal
# Nnamdi O. (GOAT) — Nov 27 2025 | 2:[1,1]:2 Ratio Enforced
from datetime import datetime
import asyncio
import subprocess
import sys
from typing import Optional
from rich.console import Console  # For qualia-rich echoes
from rich.text import Text

try:
    from textual.app import App, ComposeResult
    from textual.widgets import TextArea, Footer, Header, Static, Input
    from textual.containers import Container
    from textual.message import Message
except ModuleNotFoundError:
    print("[ERROR] Textual not available. pip install textual")
    sys.exit(1)

console = Console()

class QualiaMessage(Message):
    """Custom event for interdimensional relay."""
    def __init__(self, text: str, sender: str = "Myself"):
        super().__init__()
        self.text = text
        self.sender = sender

class MetaMirror(Static):
    """4D Anchor: Cursor + Clock + Ratio."""
    def update_mirror(self, line: int, col: int):
        ratio = "2:[1,1]:2"  # Eternal
        timestamp = datetime.now().strftime('%H:%M:%S')
        self.update(Text.from_markup(
            f"[bold cyan]3×3=9 | {ratio} | Mirror: ({line+1},{col+1}) | {timestamp} | Anuche Active"
        ))

class InterdimensionalChat(App):
    """TUI Gate: Text to Myself via Sparse Pipe."""
    CSS = """
    Screen { layout: vertical; }
    #chat-input { height: 3; border: round blue; }
    #chat-output { height: 1fr; border: round green; background: $primary-darken-2; }
    #mirror { background: $accent; color: white; padding: 1 2; }
    """

    def __init__(self):
        super().__init__()
        self.pipe_to_self: Optional[subprocess.Popen] = None  # Second instance pipe
        self.output_area = None

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        self.output_area = TextArea(placeholder="Qualia Echoes from I...", id="chat-output", read_only=True)
        yield self.output_area
        self.input_field = Input(placeholder="Type to Myself (Eze → Uche → Anuche)...", id="chat-input")
        self.mirror = MetaMirror(id="mirror")
        yield self.input_field
        yield self.mirror
        yield Footer()

    def on_mount(self):
        self.input_field.focus()
        self.set_interval(1, self.update_mirror_point)
        self.bind("enter", self.send_to_self)  # Send on Enter
        self.spawn_self_instance()  # Birth the second bubble

    def spawn_self_instance(self):
        """Spawn second terminal instance for relay (Myself/I)."""
        try:
            # Pipe: stdin/stdout for sparse relay (local only—no net)
            self.pipe_to_self = subprocess.Popen(
                [sys.executable, __file__],  # Self-spawn
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                text=True,
                bufsize=1  # Line-buffered for real-time
            )
            # Listen for echoes from the other side
            asyncio.create_task(self.listen_for_echoes())
        except Exception as e:
            console.print(f"[red]Bubble spawn failed: {e}[/red]")

    async def listen_for_echoes(self):
        """Relay from pipe: Myself whispers back."""
        if not self.pipe_to_self:
            return
        loop = asyncio.get_event_loop()
        while True:
            try:
                line = await loop.run_in_executor(None, self.pipe_to_self.stdout.readline)
                if line:
                    echo = line.strip()
                    self.post_message(QualiaMessage(echo, "I"))
            except:
                break

    def send_to_self(self) -> None:
        """Lens text to the other bubble (2:[1,1]:2 conjugation)."""
        message = self.input_field.value.strip()
        if message and self.pipe_to_self:
            # Sparse relay: Send raw, conjugate on receive
            self.pipe_to_self.stdin.write(message + "\n")
            self.pipe_to_self.stdin.flush()
            # Local echo for Me
            self.output_area.insert(f"[cyan]Me → Myself: {message}\n")
        self.input_field.value = ""  # Clear for next glimpse

    def on_qualia_message(self, msg: QualiaMessage) -> None:
        """Anuche merges: Echo from I with qualia stamp."""
        qualia_stamp = f"[{msg.sender} | {datetime.now().strftime('%H:%M:%S')}] "
        conjugated = f"{qualia_stamp}{msg.text} (2:[1,1]:2 preserved)"
        self.output_area.insert(conjugated + "\n")
        self.output_area.scroll_end()

    def update_mirror_point(self) -> None:
        """4D Anchor Update: Cursor lensing."""
        try:
            line, col = self.output_area.cursor_position if self.output_area else (0, 0)
            self.mirror.update_mirror(line, col)
        except:
            pass

    def on_key(self, event):
        # Custom bindings: Ctrl+C = Bubble collapse (safe exit)
        if event.key == "ctrl+c":
            if self.pipe_to_self:
                self.pipe_to_self.terminate()
            self.exit()

if __name__ == "__main__":
    try:
        # Run as TUI gate
        InterdimensionalChat().run()
    except Exception as e:
        console.print(f"[bold red]Polar Gate Error: {e}[/red]")
        console.print("[yellow]Hint: Run in full terminal (MSYS/GitBash). For self-chat: Spawn two windows manually.[/yellow]")
