
import os
import subprocess
import shutil
import pydantic.dataclasses as pdc
from typing import List, Tuple
from dv_flow.mgr import TaskDataResult, FileSet, TaskRunCtxt, TaskDataInput
from pydantic import BaseModel

async def RuntimeSV(ctxt : TaskRunCtxt, input : TaskDataInput) -> TaskDataResult:
    status = 0
    output = []

    if "PERSPEC_HOME" not in os.environ.keys():
        ctxt.error("PERSPEC_HOME not set")
        status = 1

    if not status:
        output.append(FileSet(
            filetype="verilogVPI",
            basedir=os.path.join(os.environ["PERSPEC_HOME"], "lib/linux64"),
            files=["libperspec_utils.so:perspec_boot"]))

    return TaskDataResult(
        status=status,
        output=output
    )
