import asyncio
from fastmcp import FastMCP
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any

from .io import io_mcp
from .pp import pp_mcp
from .tl import tl_mcp
from .pl import pl_mcp
from .util import ul_mcp



class AdataState:
    def __init__(self):
        self.adata_dic = {}
        self.active_id = None

    def get_adata(self, sampleid=None):
        if self.active_id is None:
            return None
        sampleid = sampleid or self.active_id
        return self.adata_dic[sampleid]
    
    def set_adata(self, adata, sampleid=None):
        sampleid = sampleid or self.active_id
        self.adata_dic[sampleid] = adata


ads = AdataState()

@asynccontextmanager
async def adata_lifespan(server: FastMCP) -> AsyncIterator[Any]:
    yield ads


scanpy_mcp = FastMCP("Scanpy-MCP-Server", lifespan=adata_lifespan)


async def setup():
    await scanpy_mcp.import_server("io", io_mcp)
    await scanpy_mcp.import_server("pp", pp_mcp)
    await scanpy_mcp.import_server("tl", tl_mcp) 
    await scanpy_mcp.import_server("pl", pl_mcp) 
    await scanpy_mcp.import_server("ul", ul_mcp)