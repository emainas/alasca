import subprocess, sys
def test_help():
    out = subprocess.run(
        [sys.executable, "-m", "alasca.contacts", "--help"],
        capture_output=True, text=True
    )
    assert "usage" in out.stdout.lower()
