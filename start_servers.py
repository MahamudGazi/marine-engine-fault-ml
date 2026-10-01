import subprocess
import time
import sys
import os
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent

def main():
    print("=" * 60)
    print("🚢 MARINE ENGINE FAULT ML SYSTEM - FULL STACK LAUNCHER")
    print("=" * 60)
    
    python_exe = str(ROOT_DIR / "venv" / "Scripts" / "python.exe")
    if not os.path.exists(python_exe):
        python_exe = sys.executable

    # 1. Start Django Backend
    print("[1/2] Starting Django REST Backend on http://localhost:8000 ...")
    backend_proc = subprocess.Popen(
        [python_exe, "manage.py", "runserver", "0.0.0.0:8000"],
        cwd=str(ROOT_DIR / "backend" / "django_project")
    )

    time.sleep(2)

    # 2. Start React Vite Frontend
    print("[2/2] Starting React Dashboard on http://localhost:3000 ...")
    frontend_proc = subprocess.Popen(
        ["npm", "run", "dev"],
        cwd=str(ROOT_DIR / "frontend" / "react-dashboard"),
        shell=True
    )

    print("\n✅ System running! Press Ctrl+C to terminate both servers.")
    print("👉 Frontend: http://localhost:3000")
    print("👉 Backend API: http://localhost:8000/api/\n")

    try:
        backend_proc.wait()
        frontend_proc.wait()
    except KeyboardInterrupt:
        print("\nStopping servers...")
        backend_proc.terminate()
        frontend_proc.terminate()

if __name__ == "__main__":
    main()
