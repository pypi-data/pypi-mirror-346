import os
import subprocess
import shutil
import pydantic.dataclasses as pdc
from typing import List, Tuple
from dv_flow.mgr import TaskDataResult, FileSet, TaskRunCtxt, TaskDataInput
from pydantic import BaseModel

class Memento(BaseModel):
    files : List[Tuple[str,float]] = pdc.Field(
        default_factory=list,
        description="List of files and their timestamps")

async def GenActorSV(ctxt : TaskRunCtxt, input : TaskDataInput) -> TaskDataResult:
    status = 0
    changed = (input.changed or input.memento is None) 
    memento = None
    output = []

    zuspec = shutil.which("zuspec")

    if zuspec is None:
        status = 1
        ctxt.error("zuspec not found in PATH")

    files = []
    if not status:
        for fs in input.inputs:
            if fs.filetype == "pssSource":
                for f in fs.files:
                    files.append(os.path.join(fs.basedir, f))

        if len(files) == 0:
            status = 1
            ctxt.error("No PSS files provided")

    if not status and not changed:
        try:
            memento = Memento(**input.memento)
        except Exception as e:
            changed = True

        for path,timestamp in memento.files:
            if path not in files:
                changed = True
                break
            elif os.path.getmtime(path) > timestamp:
                changed = True
                break

    if not changed:
        # Determine whether we need to run
        pass

    if changed and not status:
        root_action = input.params.root_action

        cmd = [
            zuspec,
            'synth.sv.actor',
            '-action', root_action
        ]
        cmd.extend(files)

        status |= await ctxt.exec(cmd=cmd, logfile='zuspec_synth_sv_actor.log')

    if not status:
        if changed:
            memento = Memento()
            for f in files:
                memento.files.append((f, os.path.getmtime(f)))

        output.append(FileSet(
            basedir=input.rundir,
            filetype="systemVerilogSource",
            files=["actor.sv"]
        ))


    return TaskDataResult(
        status=status,
        output=[
            FileSet(
                filetype="systemVerilogSource",
                basedir=input.rundir,
                files=[
                    "pss_top_sv.sv"
                ]
            )
        ],
        changed=changed,
        memento=memento
    )
