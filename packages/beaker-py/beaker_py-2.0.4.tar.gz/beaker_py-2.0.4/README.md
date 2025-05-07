# Beaker-py [![](https://img.shields.io/pypi/v/beaker-py)](https://pypi.org/project/beaker-py/)

A lightweight pure-Python client for Beaker.

## Installing

### Installing with `pip`

**beaker-py** is available [on PyPI](https://pypi.org/project/beaker-py/). Just run

```bash
pip install beaker-py
```

### Installing from source

To install **beaker-py** from source, first clone [the repository](https://github.com/allenai/beaker):

```bash
git clone https://github.com/allenai/beaker.git
```

Then create or activate a Python virtual environment, and run:

```bash
cd beaker/bindings/python
make dev-install
```

## Quick start

If you've already configured the [Beaker command-line client](https://github.com/allenai/beaker/),
**beaker-py** will find and use the existing configuration file (usually located at `$HOME/.beaker/config.yml`) or `BEAKER_TOKEN` environment variable.

Then you can instantiate the Beaker client with the `.from_env()` class method:

```python
from beaker import Beaker

with Beaker.from_env() as beaker:
    ...
```

With the Python client, you can:
- Query [**Clusters**](https://beaker-docs.apps.allenai.org/concept/clusters.html) with `beaker.cluster.*` methods, e.g. `beaker.cluster.get("ai2/jupiter-cirrascale-2")`.
- Manage [**Datasets**](https://beaker-docs.apps.allenai.org/concept/datasets.html) with `beaker.dataset.*` methods, e.g. `beaker.dataset.create(dataset_name, source_dir)`.
- Submit, track, and find [**Experiments**](https://beaker-docs.apps.allenai.org/concept/experiments.html) with `beaker.experiment.*`, `beaker.workload.*`, and `beaker.job.*` methods, e.g. `beaker.experiment.create(spec=spec, name=name)`.
- Manage [**Workspaces**](https://beaker-docs.apps.allenai.org/concept/workspaces.html) with `beaker.workspace.*` methods, e.g. `beaker.workspace.create("ai2/new_workspace")`.
- Manage [**Secrets**](https://beaker-docs.apps.allenai.org/concept/secrets.html) with `beaker.secret.*` methods, e.g. `beaker.secret.write(name, value)`.

### Example workflow

Launch and follow an experiment like [beaker-gantry](https://github.com/allenai/beaker-gantry) does:

```python
import time
from beaker import Beaker, BeakerExperimentSpec, BeakerJobPriority


with Beaker.from_env() as beaker:
    # Build experiment spec...
    spec = BeakerExperimentSpec.new(
        description="beaker-py test run",
        beaker_image="petew/hello-world",
        priority=BeakerJobPriority.low,
        preemptible=True,
    )

    # Create experiment workload...
    workload = beaker.experiment.create(spec=spec)

    # Wait for job to be created...
    while (job := beaker.workload.get_latest_job(workload)) is None:
        print("waiting for job to start...")
        time.sleep(1.0)

    # Follow logs...
    print("Job logs:")
    for job_log in beaker.job.logs(job, follow=True):
        print(job_log.message.decode())
```

## Development

After [installing from source](#installing-from-source), you can run checks and tests locally with:

```bash
make checks
```

### Releases

At the moment releases need to be published manually by following these steps:

1. Ensure you've authenticated with [PyPI](https://pypi.org/) through a `~/.pypirc` file and have write permissions to the [beaker-py project](https://pypi.org/project/beaker-py/).
2. Ensure the target release version defined in `src/beaker/version.py` is correct, or change the version on the fly by adding the `Make` argument `BEAKER_PY_VERSION=X.X.X` to the command in the next step.
3. Ensure the CHANGELOG.md has a section at the top for the new release (`## vX.X.X - %Y-%m-%d`).
4. Run `make publish` for a stable release or `make publish-nightly` for a nightly pre-release.
