#!/usr/bin/env python3
"""
Copy steps to a new run.

In HADDOCK3 you can copy successful steps from a run directory to a new
directory and use them as starting points for a new run.

Considering the example:

run1/
    0_topoaa/
    1_rigidbody/
    2_caprieval/
    3_seletop/
    4_flexref/
    (etc...)

You can use `4_flexref` step folder as a starting point for a new run.

USAGE::

    haddock3-copy -r <run_dir> -m <num_modules> -o <new_run_dir>
    haddock3-copy -r run1 -m 0 4 -o run2

Where, `-m 0 4` will copy `0_topoaa` and `4_flexref` to <new_run_dir>.

**Note:** If the new run uses CNS-dependent modules, you **also need**
to copy the folder corresponding to the initial topology creation (the
`topoaa` module).

`haddock3-copy` will also copy the corresponding files in the `data`
directory and update the file contents in the copied folder such that
the information on the run directory and the new step folder names match.
The output result of the above commands is:

run2/
    0_topoaa/
    1_flexref/

Following, you can use the `haddock3` command with the `--restart-from-dir`
option to continue a new run::

    haddock3 new-config.cfg --restart-from-dir run2
"""
import argparse
import sys

from haddock import log
from haddock.libs.libcli import add_version_arg


# Command line interface parser
ap = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    )

ap.add_argument(
    "-r",
    "--run-dir",
    help="The input run directory.",
    required=True,
    )

ap.add_argument(
    "-m",
    "--modules",
    nargs="+",
    help="The number of the steps to copy.",
    required=True,
    type=int,
    )

ap.add_argument(
    "-o",
    "--output",
    help="The new run directory.",
    required=True,
    )

add_version_arg(ap)


def _ap():
    return ap


def load_args(ap):
    """Load argument parser args."""
    return ap.parse_args()


def cli(ap, main):
    """Command-line interface entry point."""
    cmd = load_args(ap)
    main(**vars(cmd))


def maincli():
    """Execute main client."""
    cli(ap, main)


def main(run_dir, modules, output):
    """."""
    from pathlib import Path
    from shutil import copytree

    from haddock.gear.zerofill import zero_fill
    from haddock.modules import get_module_steps_folders

    log.info("Reading input run directory")
    # get the module folders from the run_dir input
    steps = get_module_steps_folders(run_dir)
    selected_steps = [steps[i] for i in range(len(steps)) if i in modules]
    log.info(f"selected steps: {', '.join(selected_steps)}")

    # make new run dir
    outdir = Path(output)
    try:
        outdir.mkdir(parents=True)
    except FileExistsError:
        log.error(f"Directory {str(outdir.resolve())} already exists.")
        sys.exit(1)
    log.info(f"Created directory: {str(outdir.resolve())}")

    # copy folders over
    zero_fill.set_zerofill_number(len(selected_steps))
    for i, step in enumerate(selected_steps):
        ori = Path(run_dir, step)
        _modname = step.split("_")[-1]
        dest = Path(outdir, zero_fill.fill(_modname, i))
        copytree(ori, dest)
        log.info(f"Copied {str(ori)} -> {str(dest)}")

    # copy data folders
    for i, step in enumerate(selected_steps):
        ori = Path(run_dir, "data", step)
        _modname = step.split("_")[-1]
        dest = Path(outdir, "data", zero_fill.fill(_modname, i))
        copytree(ori, dest)
        log.info(f"Copied {str(ori)} -> {str(dest)}")

    # update step names in files
    # update run dir names in files
    new_steps = get_module_steps_folders(outdir)
    for psf, ns in zip(selected_steps, new_steps):
        new_step = Path(outdir, ns)
        for file_ in new_step.iterdir():
            text = file_.read_text()
            new_text = text.replace(psf, ns)
            new_text = new_text.replace(run_dir, output)
            file_.write_text(new_text)

    log.info("File references updated correctly.")

    return


if __name__ == "__main__":
    sys.exit(maincli())
