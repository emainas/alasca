import subprocess, sys

def test_contacts_help():
    out = subprocess.run(
        [sys.executable, "-m", "alasca.cli", "contacts", "--help"],
        capture_output=True, text=True
    )
    assert "usage" in out.stdout.lower()
