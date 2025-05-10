
import os
import subprocess
import shutil
import pydantic.dataclasses as pdc
from typing import List, Tuple
from dv_flow.mgr import TaskDataResult, FileSet, TaskRunCtxt, TaskDataInput
from dv_flow.libpss.psp_log_parser import PspLogParser
from pydantic import BaseModel

class Memento(BaseModel):
    files : List[Tuple[str,float]] = pdc.Field(
        default_factory=list,
        description="List of files and their timestamps")

async def Lib(ctxt : TaskRunCtxt, input : TaskDataInput) -> TaskDataResult:
    status = 0
    changed = (input.changed or input.memento is None)
    memento = None
    output = []
    markers = []

    perspec = shutil.which("perspec")

    if perspec is None:
        status = 1
        ctxt.error("'perspec' not found in PATH")

    files = []
    if not status:
        for fs in input.inputs:
            if fs.filetype == "pssSource":
                for f in fs.files:
                    files.append(os.path.join(fs.basedir, f))
        if len(files) == 0:
            status = 1
            ctxt.error("No PSS files provided")

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
        cmd = [perspec, 'save', '-snapshot', 'snapshot.psv']
        for file in files:
            cmd.extend(['-pss', file])

        status |= await ctxt.exec(
            cmd=cmd,
            logfile="perspec_save.log",
            logfilter=PspLogParser(ctxt).line)

    memento = Memento()
    for file in files:
        memento.files.append((file, os.path.getmtime(file)))
    
    output.append(FileSet(
        basedir=input.rundir,
        filetype="pssLib",
        files=['snapshot.psv']))

    return TaskDataResult(
        changed=changed,
        status=status,
        memento=memento,
        output=output,
        markers=markers
    )
