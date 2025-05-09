import os
import tempfile
from pykeflow import Workflow, Job, Step
from ruamel.yaml.scalarstring import LiteralScalarString

def test_step_to_dict():
    s1 = Step(name="Say hello", run="echo Hello")
    s2 = Step(name="Multiline", run="echo Hi\necho Bye", with_args={"arg1": "val"})

    d1 = s1.to_dict()
    d2 = s2.to_dict()

    assert d1["name"] == "Say hello"
    assert d1["run"] == "echo Hello"
    assert isinstance(d2["run"], LiteralScalarString)  # Updated line
    assert d2["with"]["arg1"] == "val"


def test_job_to_dict():
    step = Step(name="Test", run="echo ok")
    job = Job(id="build", runs_on="ubuntu-latest", steps=[step])
    job_dict = job.to_dict()

    assert job_dict["runs-on"] == "ubuntu-latest"
    assert len(job_dict["steps"]) == 1
    assert job_dict["steps"][0]["name"] == "Test"

def test_workflow_dict_and_yaml():
    step = Step(name="Run tests", run="pytest")
    job = Job(id="test", runs_on="ubuntu-latest", steps=[step])
    wf = Workflow(name="CI", on=["push", "pull_request"], jobs=[job])

    wf_dict = wf.to_dict()
    assert wf_dict["name"] == "CI"
    assert "on" in wf_dict
    assert "jobs" in wf_dict

    yaml_str = wf.to_yaml()
    assert "name: CI" in yaml_str
    assert "on:" in yaml_str
    assert "test:" in yaml_str

def test_round_trip_yaml():
    step = Step(name="Build", run="make all")
    job = Job(id="build", runs_on="ubuntu-latest", steps=[step])
    wf = Workflow(name="Build Workflow", on=['push'], jobs=[job])

    yaml_str = wf.to_yaml()
    print(yaml_str,wf.to_dict())  # For debugging purposes
    new_wf = Workflow.from_yaml(yaml_str)
    print(new_wf,new_wf.to_yaml())  # For debugging purposes

    assert new_wf.name == wf.name
    assert new_wf.on == wf.on
    assert len(new_wf.jobs) == 1
    assert new_wf.jobs[0].runs_on == "ubuntu-latest"

def test_save_to_file():
    step = Step(name="Save test", run="echo saving")
    job = Job(id="save", runs_on="ubuntu-latest", steps=[step])
    wf = Workflow(name="Save Flow", on=["push"], jobs=[job])

    with tempfile.TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, "workflow.yml")
        wf.save(path)
        assert os.path.exists(path)
        with open(path) as f:
            contents = f.read()
        assert "Save Flow" in contents
