import subprocess

def start_roblox():
    try:
        subprocess.Popen(r"C:\Users\Simon\AppData\Local\Roblox\Versions\version-c3c1514fd260482e\RobloxPlayerBeta.exe")
        print("🎮 Roblox starting...")
    except Exception as e:
        print(f"💥 Error: {e}")

def studio_roblox():
    try:
        subprocess.Popen(r"C:\Users\Simon\AppData\Local\Roblox\Versions\version-c3c1514fd260482e\RobloxStudioBeta.exe")
        print("🛠️ Starting Roblox Studio...")
    except Exception as e:
        print(f"💥 Error: {e}")
