
import os
import subprocess
import shutil
import pydantic.dataclasses as pdc
from typing import List, Tuple
from dv_flow.libpss.psp_log_parser import PspLogParser
from dv_flow.mgr import TaskDataResult, FileSet, TaskRunCtxt, TaskDataInput
from pydantic import BaseModel

class Memento(BaseModel):
    files : List[Tuple[str,float]] = pdc.Field(
        default_factory=list,
        description="List of files and their timestamps")

async def GenModelSV(ctxt : TaskRunCtxt, input : TaskDataInput) -> TaskDataResult:
    status = 0
    changed = (input.changed or input.memento is None)
    memento = None
    output = []
    markers = []

    changed = True

    perspec = shutil.which("perspec")

    if perspec is None:
        status = 1
        ctxt.error("'perspec' not found in PATH")

    if "VCS_HOME" not in os.environ.keys():
        status = 1
        ctxt.error("'VCS_HOME' not set")
    else:
        vcs_home = os.environ["VCS_HOME"]

    files = []
    libs = []
    if not status:
        for fs in input.inputs:
            if fs.filetype == "pssSource":
                for f in fs.files:
                    files.append(os.path.join(fs.basedir, f))
            elif fs.filetype == "pssLib":
                for f in fs.files:
                    libs.append(os.path.join(fs.basedir, f))

        if len(libs) and len(files):
            ctxt.error("Both libraries and sources provided")
            status = 1
        elif not len(libs) and not len(files):
            ctxt.error("Neither libraries and sources provided")
            status = 1
        elif len(libs) > 1:
            ctxt.error("Only one library can be provided")
            status = 1

    if not changed and not status:
        try:
            ex_memento = Memento(**input.memento)

            if len(files) == len(ex_memento.files):
                for file in ex_memento.files:
                    if file[0] not in files:
                        changed = True
                    elif os.path.getmtime(file[0]) > file[1]:
                        changed = True
                    if changed:
                        break
            else:
                changed = True
        except Exception as e:
            changed = True

    if changed and not status:
        cmd = [perspec, 'generate', '-top_action', 'pss_top::Null']
        
        for lib in libs:
            cmd.extend(['-restore', lib])
        for file in files:
            cmd.extend(['-pss', file])

        status |= await ctxt.exec(
            cmd=cmd,
            logfile="perspec_gen.log",
            logfilter=PspLogParser(ctxt).line)

    if changed and not status:
        cmd = ['gcc', 
               '-fPIC', '-shared',
               '-I%s/target_dir_1' % input.rundir,
               '-I%s/include' % vcs_home,
               '%s/target_dir_1/perspec_sv_test.c' % input.rundir,
               '-o', '%s/libpss_null_test.so' % input.rundir]
        status |= await ctxt.exec(cmd, 'nulltest.log')

    memento = Memento()
    for file in files:
        memento.files.append((file, os.path.getmtime(file)))
    
    output.append(FileSet(
        basedir=input.rundir,
        filetype="systemVerilogSource",
        files=[
            'target_dir_1/perspec_pkg.sv',
            'target_dir_1/perspec_top.sv',
            'target_dir_1/perspec_exports.sv',
        ]))

    return TaskDataResult(
        changed=changed,
        status=status,
        memento=memento,
        output=output,
        markers=markers
    )

