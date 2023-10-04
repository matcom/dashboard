#%%
import yaml
from pathlib import Path

projects = []

for fname in Path("../data/Project").rglob("*.yaml"):
    with fname.open() as fp:
        data = yaml.safe_load(fp)
        projects.append(data)

# %%
for project in projects:
    print(repr(project['title']), ",", repr(project['project_type']), ",", repr(project['program']))

# %%
groups = []

for fname in Path("../data/ResearchGroup").rglob("*.yaml"):
    with fname.open() as fp:
        data = yaml.safe_load(fp)
        groups.append(data)

# %%
for group in groups:
    print(repr(group['name']), ",", repr(len(group['members'])))
