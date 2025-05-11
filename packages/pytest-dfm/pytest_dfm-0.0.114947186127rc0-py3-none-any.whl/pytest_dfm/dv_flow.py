import asyncio
import os
import dataclasses as dc
import logging
from pytest import FixtureRequest
from dv_flow.mgr import PackageLoader, TaskGraphBuilder, TaskSetRunner
from typing import ClassVar

@dc.dataclass
class DvFlow(object):
    request: FixtureRequest
    srcdir : str
    tmpdir: str
    builder : TaskGraphBuilder = dc.field(default=None)
    _log : ClassVar = logging.getLogger("DvFlow")

    def __post_init__(self):
        self.builder = TaskGraphBuilder(None, self.tmpdir)
        self.srcdir = os.path.dirname(self.request.fspath)
        pass

#    def addOverride(self, key, value):
#        self.builder.addOverride(key, value)

    def loadPkg(self, pkgfile):
        """Loads the specified flow.dv file as th root package"""
        loader = PackageLoader()
        pkg = loader.load(pkgfile)
        self.builder = TaskGraphBuilder(pkg, self.tmpdir, loader=loader)

    def mkTask(self, 
                   task_t,
                   name=None,
                   srcdir=None,
                   needs=None,
                   **kwargs):
        """Creates a task of the specified type"""
        return self.builder.mkTaskNode(
            task_t, 
            name=name, 
            srcdir=srcdir, 
            needs=needs, 
            **kwargs)

    def runTask(self, 
                task, 
                listener=None,
                nproc=-1):
        """Executes the specified tree of task nodes"""
        markers = []
        runner = TaskSetRunner(self.tmpdir)

        def local_listener(task, reason):
            if reason == "leave":
                markers.extend(task.result.markers)

        if listener is not None:
            runner.add_listener(listener)
        else:
            runner.add_listener(local_listener)

        if nproc != -1:
            runner.nproc = nproc

        ret = asyncio.run(runner.run(task))

        # Display markers
        for m in markers:
            print("Marker: %s" % m.msg)

        return (runner.status, ret)


