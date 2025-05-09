import os
import subprocess
import shutil
from dv_flow.mgr import TaskDataResult, FileSet
from pydantic import BaseModel

class Memento(BaseModel):
    share_dir : str

async def RuntimeSV(ctxt, input):
    # First, see if zuspec is installed in this Python interpreter
    status = 0
    output = []
    memento = None
    share_dir = None
    ex_memento = None

    if input.memento is not None:
        try:
            ex_memento = Memento(**input.memento)
        except Exception as e:
            pass 

    if ex_memento is not None and os.path.isdir(ex_memento.share_dir):
        share_dir = ex_memento.share_dir

    if share_dir is None:
        if shutil.which("zuspec") is None:
            status = 1
            ctxt.error("zuspec not found in PATH")

        if not status:
            cmd = ['zuspec', 'synth.sv.share']

            try:
                ret = subprocess.check_output(cmd)
                share_dir = ret.decode().strip()
            except Exception as e:
                ctxt.error("Failed to run zuspec command: %s" % str(e))
                status = 1

    memento = Memento(share_dir=share_dir)
            
    output.append(FileSet(
        filetype="systemVerilogSource",
        basedir=os.path.join(share_dir, "include/zsp/sv/zsp_sv"),
        files=[
            "zsp_sv.sv"
        ]))

    return TaskDataResult(
        status=status,
        output=output,
        memento=memento
    )
