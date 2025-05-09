import sys


class Console:

    @staticmethod
    def write_stdout(message: str = "", end: str = "\n"):
        sys.stdout.write(f"{message}{end}")

    @staticmethod
    def write_stderr(message: str = "", end: str = "\n"):
        sys.stderr.write(f"{message}{end}")
