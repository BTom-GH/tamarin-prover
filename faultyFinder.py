import glob
import subprocess

for f in glob.glob("case-studies/fast-tests/**/*.spthy"):
    print(f"Testing {f}")
    cmd = [
        "~/.local/bin/tamarin-prover",
        f,
        "--prove",
        "--stop-on-trace=dfs",
        "+RTS", "-N3", "-RTS",
        "-o" + f + ".tmp"
    ]
    try:
        subprocess.run(" ".join(cmd), shell=True, check=True)
    except subprocess.CalledProcessError:
        print(f"FAILED: {f}")