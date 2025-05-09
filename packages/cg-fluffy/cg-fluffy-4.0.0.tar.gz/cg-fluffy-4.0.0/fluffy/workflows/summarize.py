"""Summarize the analysis"""

import logging
import os
import sys

from pathlib import Path

from fluffy.slurm_api import SlurmAPI
from fluffy.commands.multiqc import get_multiqc_cmd
from fluffy.singularity_cmd import singularity_base

LOG = logging.getLogger(__name__)	

def get_summarize_cmd(
    singularity: str, out_dir: Path, outfile: str,project_id: str, sample_sheet: str, zscore: str, mincnv: str, maxgcd: float,maxatd: float,maxbin2bin: float, maxdup: float, minreads:int
) -> str:
    """Return a string with the command to summarize a run"""

    wd=os.path.dirname(os.path.realpath(__file__)).replace("fluffy/workflows","fluffy/scripts")
    python_path=os.path.realpath(sys.executable)

    summary_cmd = (
        f"{python_path} {wd}/generate_csv.py "
        f"--folder {str(out_dir)} --samplesheet {sample_sheet} --Zscore {zscore} --minCNV {mincnv} --maxGCD {maxgcd} --maxATD {maxatd} --maxbin2bin {maxbin2bin} --maxdup {maxdup} --minreads {minreads} "
        f"> {outfile}"
    )
    return summary_cmd

def get_two_pass_ref_cmd(
    singularity: str,
    out_dir: Path,
    project_id: str,
    working_directory: str, 
    preface_bin_size: int,
    wisecondor_bin_size: int,
    ) -> str:

    outfile = out_dir / f"{project_id}.1pass.csv"
    python_path=os.path.realpath(sys.executable)

    two_bass_ref_cmd = (
        f"{python_path} {working_directory}/filter_csv.py --csv {outfile} --project {out_dir} --singularity \"{singularity}\" --binsize {preface_bin_size} {wisecondor_bin_size}"
    )
    
    return(two_bass_ref_cmd)

def get_merge_cmd(
    singularity: str,
    out_dir: Path,
    project_id: str,
    working_directory: str, 
    ) -> str:

    outfile = out_dir / f"{project_id}.csv"
    first_pass = out_dir / f"{project_id}.1pass.csv"
    second_pass = out_dir / f"{project_id}.2pass.csv"
    python_path=os.path.realpath(sys.executable)

    merge_cmd = (
        f"{python_path} {working_directory}/merge_csv.py {first_pass} {second_pass} > {outfile}"
    )
    
    return(merge_cmd)


def summarize_workflow(
    configs: dict, afterok: list, slurm_api: SlurmAPI, dry_run: bool = False,batch_ref: bool=False,two_pass: bool = False, 
) -> int:
    """Run the workflow to summarize an analysis"""
    LOG.info("Run the summarize workflow")
    out_dir = configs["out"]
    project_id=configs["project_id"]

    singularity=singularity_base(configs["singularity"], configs["out"], configs["project"], configs["singularity_bind"])

    wd=os.path.dirname(os.path.realpath(__file__)).replace("fluffy/workflows","fluffy/scripts")

    if not two_pass:
        multiqc_cmd=get_multiqc_cmd(singularity=singularity,input_dir=out_dir,out_dir=out_dir)
        if batch_ref:

            outfile = out_dir / f"{project_id}.2pass.csv"
            summarize_cmd = get_summarize_cmd(
                singularity=singularity,
                out_dir=out_dir,
                outfile=outfile,
                project_id=configs["project_id"],
                sample_sheet=configs["sample_sheet"],
                zscore=configs["summary"]["zscore"],
                mincnv=configs["summary"]["mincnv"],
                maxgcd=configs["summary"]["maxGCD"],
                maxatd=configs["summary"]["maxATD"],
                maxbin2bin=configs["summary"]["maxbin2bin"],
                maxdup=configs["summary"]["maxdup"],
                minreads=configs["summary"]["minreads"]
            )

            merge_cmd=get_merge_cmd(singularity,out_dir,configs["project_id"],wd)
            command_str=f"{multiqc_cmd}\n{summarize_cmd}\n{merge_cmd}"

        else:
            outfile = out_dir / f"{project_id}.csv"
            summarize_cmd = get_summarize_cmd(
                singularity=singularity,
                out_dir=out_dir,
                outfile=outfile,
                project_id=configs["project_id"],
                sample_sheet=configs["sample_sheet"],
                zscore=configs["summary"]["zscore"],
                mincnv=configs["summary"]["mincnv"],
                maxgcd=configs["summary"]["maxGCD"],
                maxatd=configs["summary"]["maxATD"],
                maxbin2bin=configs["summary"]["maxbin2bin"],
                maxdup=configs["summary"]["maxdup"],
                minreads=configs["summary"]["minreads"]
            )
            command_str=f"{multiqc_cmd}\n{summarize_cmd}"

    else:
        outfile = out_dir / f"{project_id}.1pass.csv"
        summarize_cmd = get_summarize_cmd(
            singularity=singularity,
            out_dir=out_dir,
            outfile=outfile,
            project_id=configs["project_id"],
            sample_sheet=configs["sample_sheet"],
            zscore=configs["summary"]["zscore"],
            mincnv=configs["summary"]["mincnv"],
            maxgcd=configs["summary"]["maxGCD"],
            maxatd=configs["summary"]["maxATD"],
            maxbin2bin=configs["summary"]["maxbin2bin"],
            maxdup=configs["summary"]["maxdup"],
            minreads=configs["summary"]["minreads"]

        )


        build_two_pass_ref=get_two_pass_ref_cmd(singularity,out_dir,configs["project_id"],wd,configs["wisecondorx"]["testbinsize"],configs["wisecondorx"]["prefacebinsize"])
        command_str=f"{summarize_cmd}\n{build_two_pass_ref}"


    jobid = slurm_api.run_job(
        name=f"summarize_batch",
        command=command_str,
        afterok=afterok,
        dry_run=dry_run,
    )

    return jobid
