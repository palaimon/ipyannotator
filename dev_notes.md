## env setup


To install lib and deps use:

`poetry install`

if you want to use jupyterlab also install widget support either in lab
using extension manager of with
`poetry run jupyter labextension install @jupyter-widgets/jupyterlab-manager`

Make sure to setup nbstripout filters just after repo clone:
 
```
poetry run nbstripout --install
```

This will install git hook that automatically strips output from `.ipynb` files
on-the-fly when commited. The output will remain in working copy.

To modify local files inplace: 

```
nbstripout FILE.ipynb [FILE2.ipynb ...]
```

To mark special cells so that the output is not stripped:

Set the `keep_output` tag on the cell. 
To do this, enable the tags toolbar in jupyter notebook (`View > Cell Toolbar > Tags`) and then add the `keep_output` tag for each cell you would like to keep the output for.

You can also keep output for an entire notebook. 
To do so, add the option:
 ```
{
  "keep_output": true,
}
```

to the notebook metadata (`Edit > Edit Notebook Metadata`) 

### How To build lib:

```
nbdev_build_lib
```

or add the last cell to ipynb file:

```
from nbdev.export import *
notebook2script()
```

## Folder Outline


folders managed by git-annex

```bash
.
├── data
│   ├── converted # normaelized data used for modeling and analysis
│   └── raw # complete raw input data
├── materials
│   ├── html_nbs # html rendered nb including output
│   └── slides # rendered slides
└── models
    ├── dev # models shared for dev
    └── release # models deployed / externaly shared
```


## Deffered poetry whl install on CI:

1. Do not install binary on docker build step:  

    https://gitlab.palaimon.io/fastfm/benchmarks2/-/blob/dc8b855315751b35c34912848c8c3700365a15f9/Dockerfile#L73

2. Enable artifacts to share binary across jobs:

    https://gitlab.palaimon.io/devops/nbdev-template/-/blob/4eee3785f28c74d8966e623c3cb9c3cae229f0f2/.gitlab-ci.yml#L55

3. Use `poetry install` to fix missing dep on next ci jobs.

## Possible issues and workarounds:

**Error:**
`NameError: name ‘IN_NOTEBOOK’ is not defined:`

**Fix:**
`poetry run pip install nbdev --upgrade` 

**Details:** https://forums.fast.ai/t/nameerror-name-in-notebook-is-not-defined/78590/3

<HR>

**Error:**
```
.venv/bin/python: No module named ipykernel_launcher
[I 10:57:14.135 NotebookApp] KernelRestarter: restarting kernel (1/5), new random ports
.venv/bin/python: No module named ipykernel_launcher
[I 10:57:17.148 NotebookApp] KernelRestarter: restarting kernel (2/5), new random ports
.venv/bin/python: No module named ipykernel_launcher
[I 10:57:20.158 NotebookApp] KernelRestarter: restarting kernel (3/5), new random ports
.venv/bin/python: No module named ipykernel_launcher

```
**Fix:**

`poetry run python -m ipykernel install --user --name <kernel_name> --display-name "<kernel_name>"`

where `<kernel_name>` - name for a new jupyter kernel
Once cerated, you can select it from jupyter notebook menu:

`Kernel -> Change Kernel -> <kernel_name>`
 
 <HR>
 
**Error:**  ipy widget or canvas are not shown in jupyter lab
 
 
**Fix:** 

Check existing extensions:

 ```jupyter labextension list```
 
Working extension list gives at least:

```
JupyterLab v2.2.8
Known labextensions:
   app dir: ipyannotator2/.venv/share/jupyter/lab
        @jupyter-widgets/jupyterlab-manager v2.0.0  enabled  OK
        ipycanvas v0.5.1  enabled  OK
        ipyevents v1.8.0  enabled  OK
        nbdime-jupyterlab v2.0.0  enabled  OK
```

For clean (re)install:

`jupyter lab clean` to remove the staging and static directories from the lab 

 _ipywidgets_:
 
 `jupyter labextension install @jupyter-widgets/jupyterlab-manager`
 
 _ipycanvas_:
 
 `jupyter labextension install @jupyter-widgets/jupyterlab-manager ipycanvas`
 
 _ipyevents_:
 
 `jupyter labextension install @jupyter-widgets/jupyterlab-manager ipyevents`
 
 _nbdime_:
 
 `nbdime extensions --enable [--sys-prefix/--user/--system]`
 
 <HR>

To automatically install `voila` together with `nbdev` an old revision can be used, however this is not included in current `pyproject.toml` file to avoid a very time consuming `git clone`, which slows down the poetry dependency resolution dramatically.

```toml
voila = { git = "https://github.com/voila-dashboards/voila.git", rev = "e23fcca926584a5aa837c3354804aa2d761edda3" }
```

Manual workaround with viola app described in `README.md`.
