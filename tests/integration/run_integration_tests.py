from pathlib import Path
from sys import exit

from pytest import main


def run_integration_tests() -> None:
    integration_tests_path = Path(__file__).resolve().parent
    exit(main([str(integration_tests_path)]))


if __name__ == "__main__":
    run_integration_tests()
