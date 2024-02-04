from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Input

class WalgreensApp(App):
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]

    def compose(self) -> ComposeResult:
        yield Header()

        yield Input(placeholder="Talk to Willow!")

        yield Footer()

    def action_toggle_dark(self) -> None:
        self.dark = not self.dark

if __name__ == "__main__":
    app = WalgreensApp()
    app.run()