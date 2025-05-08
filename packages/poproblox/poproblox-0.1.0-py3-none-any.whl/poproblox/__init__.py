from .core import start_roblox, studio_roblox

class _StartWrapper:
    def roblox(self):
        start_roblox()

class _StudioWrapper:
    def roblox(self):
        studio_roblox()

start = _StartWrapper()
studio = _StudioWrapper()

# 🔥 black magic – injectnout do globalního prostoru
import builtins
builtins.start = start
builtins.studio = studio
