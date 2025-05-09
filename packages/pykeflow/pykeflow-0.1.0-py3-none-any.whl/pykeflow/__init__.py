import os
from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import LiteralScalarString
from ruamel.yaml.comments import CommentedSeq

yaml = YAML()
yaml.preserve_quotes = True
yaml.default_flow_style = False
yaml.indent(mapping=2, sequence=4, offset=2)


# === Literal block string formatting ===
class LiteralStr(str): pass


# === Inline list formatting (for `on`) ===
class InlineList(list): pass


class Workflow:
    def __init__(self, name, on, jobs):
        self.name = name
        self.on = on
        self.jobs = jobs

    def to_dict(self):
        data = {
            'name': self.name,
            'on': self.on,
            'jobs': {job.id: job.to_dict() for job in self.jobs}
        }

        # Ensure `on` appears as an inline list if it's a list
        if isinstance(data['on'], list):
            seq = CommentedSeq(data['on'])
            seq.fa.set_flow_style()
            data['on'] = seq

        return data

    def to_yaml(self):
        from io import StringIO
        stream = StringIO()
        yaml.dump(self.to_dict(), stream)
        return stream.getvalue()

    def save(self, path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            f.write(self.to_yaml())

    @staticmethod
    def from_dict(data):
        name = data.get('name')
        on_raw = data.get('on', [])
        if isinstance(on_raw, str):
            on = [on_raw]
        elif isinstance(on_raw, (list, CommentedSeq)):
            on = list(on_raw)
        elif isinstance(on_raw, dict):
            on = dict(on_raw)
        else:
            on = []

        jobs = []
        for jid, jdata in data.get('jobs', {}).items():
            steps = []
            for sdata in jdata.get('steps', []):
                steps.append(Step(
                    name=sdata.get('name'),
                    uses=sdata.get('uses'),
                    run=sdata.get('run'),
                    with_args=sdata.get('with')
                ))
            jobs.append(Job(id=jid, runs_on=jdata.get('runs-on'), steps=steps))

        return Workflow(name, on, jobs)

    @classmethod
    def from_yaml(cls, yaml_str):
        from io import StringIO
        data = yaml.load(StringIO(yaml_str))
        return cls.from_dict(data)


class Job:
    def __init__(self, id, runs_on, steps):
        self.id = id
        self.runs_on = runs_on
        self.steps = steps

    def to_dict(self):
        return {
            'runs-on': self.runs_on,
            'steps': [step.to_dict() for step in self.steps]
        }


class Step:
    def __init__(self, name=None, uses=None, run=None, with_args=None):
        self.name = name
        self.uses = uses
        self.run = run
        self.with_args = with_args or {}

    def to_dict(self):
        data = {}
        if self.name:
            data['name'] = self.name
        if self.uses:
            data['uses'] = self.uses
        if self.run:
            data['run'] = LiteralScalarString(self.run) if '\n' in self.run else self.run
        if self.with_args:
            data['with'] = self.with_args
        return data
