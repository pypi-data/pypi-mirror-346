from snaparg import ArgumentParser
from . import Workflow, Job, Step
import os

def generate_tests_yml():
    steps = [
        Step(name="Checkout code", uses="actions/checkout@v3"),
        Step(name="Set up Python", uses="actions/setup-python@v5", with_args={"python-version": "3.x"}),
        Step(name="Install dependencies", run="pip install pytest\npip install ."),
        Step(name="Run tests", run="pytest"),
    ]
    job = Job(id="test", runs_on="ubuntu-latest", steps=steps)
    wf = Workflow(name="Run Tests", on=["push"], jobs=[job])
    wf_path = ".github/workflows/tests.yml"
    wf.save(wf_path)
    print(f"✅ Created: {wf_path}")

def main():
    parser = ArgumentParser(description="Pykeflow CLI")
    parser.add_argument("-t", "--tests", action="store_true", help="Generate .github/workflows/tests.yml")
    args = parser.parse_args()

    if args.tests:
        generate_tests_yml()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
