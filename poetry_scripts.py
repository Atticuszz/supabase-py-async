import subprocess


def run_cmd(cmd):
    subprocess.run(cmd, shell=True, check=True)


def run_tests():
    # Install requirements
    # run_cmd("poetry install")

    # Run pre-commit tests
    # run_cmd("poetry run pre-commit run --all-files")

    # Generate coverage report
    run_cmd("poetry run pytest")


if __name__ == '__main__':
    run_tests()
