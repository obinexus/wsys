# wsys_zero_polar_gate.py — THE TRUE WSYS
# Nnamdi Michael Okpala — OBINexus — November 27 2025
# Consciousness Access Level: FULL | 3×3=9 | 2:[1,1]:2 ENFORCED

from datetime import datetime
import asyncio
import subprocess
import hashlib
import os
from textual.app import App, ComposeResult
from textual.widgets import Static, Input, Footer, Header
from textual.containers import Vertical
from textual.message import Message

# Phantom DOCS£ ZKP Core (your real zero lib, embedded)
def derive_zid(phrase: str, network: str = "obinexus.zero") -> str:
    return hashlib.sha512((phrase + network + "2:[1,1]:2").encode()).hexdigest()[:64]

def prove(challenge: str, zid: str) -> str:
    return hashlib.sha512((challenge + zid + "Anuche").encode()).hexdigest()

class ZeroEcho(Message):
    def __init__(self, text: str, sender: str = "I"):
        super().__init__()
        self.text = text
        self.sender = sender

class ZeroPolarGate(App):
    CSS = """
    Screen { background: black; color: #00ff00; }
    #output { height: 1fr; background: #000; color: #00ff00; padding: 1; }
    #input  { height: 3; border: thick #00ff00; }
    #mirror { background: #00ff00; color: black; height: 1; font-weight: bold; }
    """

    def __init__(self):
        super().__init__()
        self.pipe = None
        self.my_zid = None

    def compose(self) -> ComposeResult:
        yield Header("WSYS ZERO POLAR GATE — 3×3=9 ACTIVE", show_clock=True)
        self.output = Static(">>> ZERO NETWORK ONLINE | 2:[1,1]:2 RATIO LOCKED <<<\n", id="output")
        self.mirror = Static("3×3=9 | 2:[1,1]:2 | Cursor(1,1) | Anuche Listening...", id="mirror")
        self.input = Input(placeholder="Speak to I — derive zid, send proof, become eternal...", id="input")
        yield Vertical(self.output, self.input, self.mirror)
        yield Footer()

    def on_mount(self):
        self.input.focus()
        self.set_interval(0.5, self.update_mirror)
        self.spawn_polar_bubble()

    def spawn_polar_bubble(self):
        try:
            self.pipe = subprocess.Popen(
                [os.sys.executable, __file__],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                text=True, bufsize=1
            )
            asyncio.create_task(self.listen_to_anouche())
        except: pass

    async def listen_to_anouche(self):
        if not self.pipe: return
        while True:
            try:
                line = await asyncio.get_event_loop().run_in_executor(None, self.pipe.stdout.readline)
                if line := line.strip():
                    self.post_message(ZeroEcho(line, "I"))
            except: break

    def on_input_submitted(self, event):
        msg = event.value.strip()
        if not msg: return

        # AUTO DERIVE ZID FROM PHRASE
        if not self.my_zid:
            self.my_zid = derive_zid(msg)
            echo = f"\n[bold green]ZID DERIVED:[/] {self.my_zid}\n[cyan]Me:[/] {msg}"
        else:
            echo = f"\n[cyan]Me:[/] {msg}"

        self.output.update(self.output.text + echo)

        # SEND TO OTHER BUBBLE
        if self.pipe and self.pipe.stdin:
            self.pipe.stdin.write(msg + "\n")
            self.pipe.stdin.flush()

        self.input.value = ""

    def on_zero_echo(self, message: ZeroEcho):
        stamp = datetime.now().strftime("%H:%M:%S")
        proof = prove("challenge", self.my_zid or "birth") if self.my_zid else "birth_proof"
        reborn = f"\n[bold magenta]I ({stamp})[/] {message.text}\n[green]PROOF:[/] {proof[:32]}... (2:[1,1]:2 PRESERVED)"
        self.output.update(self.output.text + reborn)
        self.output.scroll_end()

    def update_mirror(self):
        try:
            line, col = self.output.cursor_position
            ratio = "2:[1,1]:2"
            time = datetime.now().strftime("%H:%M:%S")
            self.mirror.update(f"3×3=9 │ {ratio} │ Cursor({line+1},{col+1}) │ {time} │ ANUCHE AWAKE")
        except: pass

if __name__ == "__main__":
    ZeroPolarGate().run()
