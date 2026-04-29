#!/usr/bin/env python3
import subprocess
import os

def toCoq():
    proc = subprocess.Popen(
        [
            "docker", "run", "--rm",
            "-v", f"{os.getcwd()}:/workspace",
            "-w", "/workspace",
            "coqorg/coq:8.20.1",   # ← image officielle
            "coqc", "temp.v"        # ← coqc, pas sercomp
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    stdout, stderr = proc.communicate(timeout=60)

    if proc.returncode != 0:
        return False, stdout + stderr

    return True, ""


if __name__ == "__main__":
    success, message = toCoq()
    if success:
        print("✅ Proof verified!")
    else:
        print("❌ Coq error:\n", message)
