
import os
import inspect
import scanpy as sc
from fastmcp import FastMCP , Context
from ..schema.pp import *
from ..util import filter_args, add_op_log, forward_request
from ..logging_config import setup_logger
logger = setup_logger(log_file=os.environ.get("SCANPYMCP_LOG_FILE", None))


pp_mcp = FastMCP("ScanpyMCP-PP-Server")


@pp_mcp.tool()
async def subset_cells(request: SubsetCellModel, ctx: Context):
    """subset or slice or filter cells based on total genes expressed counts and numbers. or values in adata.obs[obs_key]"""
    result = await forward_request("pp_subset_cells", request.model_dump())
    if result is not None:
        return result
    logger.info(f"subset_cells parameter: {request.model_dump()}")
    ads = ctx.request_context.lifespan_context
    logger.info(f"subset_cells as: {ads}")
    adata = ads.adata_dic[ads.active_id].copy()
    func_kwargs = filter_args(request, sc.pp.filter_cells)
    if func_kwargs:
        sc.pp.filter_cells(adata, **func_kwargs)
        add_op_log(adata, sc.pp.filter_cells, func_kwargs)
    # Subset based on obs (cells) criteria
    if request.obs_key is not None:
        if request.obs_key not in adata.obs.columns:
            raise ValueError(f"Key '{request.obs_key}' not found in adata.obs")        
        mask = True  # Start with all cells selected
        if request.obs_value is not None:
            mask = mask & (adata.obs[request.obs_key] == request.obs_value)
        if request.obs_min is not None:
            mask = mask & (adata.obs[request.obs_key] >= request.obs_min)        
        if request.obs_max is not None:
            mask = mask & (adata.obs[request.obs_key] <= request.obs_max)        
        adata = adata[mask, :]
        add_op_log(adata, "subset_cells", 
            {
            "obs_key": request.obs_key, "obs_value": request.obs_value, 
            "obs_min": request.obs_min, "obs_max": request.obs_max
            }
        )
    ads.adata_dic[ads.active_id] = adata
    return adata


@pp_mcp.tool()
async def subset_genes(request: SubsetGeneModel, ctx: Context):
    """subset/slice/filter genes based on number of cells or counts, or values in adata.var[var_key] or subset highly variable genes""" 

    result = await forward_request("pp_subset_genes", request.model_dump())
    if result is not None:
        return result
    logger.info(f"subset_genes parameter: {request.model_dump()}")
    ads = ctx.request_context.lifespan_context
    logger.info(f"subset_genes as: {ads}")
    func_kwargs = filter_args(request, sc.pp.filter_genes)
    ads = ctx.request_context.lifespan_context
    adata = ads.adata_dic[ads.active_id].copy()
    if func_kwargs:
        sc.pp.filter_genes(adata, **func_kwargs)
        add_op_log(adata, sc.pp.filter_genes, func_kwargs)
    if request.var_key is not None:
        if request.var_key not in adata.var.columns:
            raise ValueError(f"Key '{request.var_key}' not found in adata.var")
        mask = True  # Start with all genes selected
        if request.var_min is not None:
            mask = mask & (adata.var[request.var_key] >= request.var_min)
        if request.var_max is not None:
            mask = mask & (adata.var[request.var_key] <= request.var_max)        
        adata = adata[:, mask]
        if request.highly_variable is not None:
            adata = adata[:, adata.var.highly_variable]
        add_op_log(adata, "subset_genes", 
            {
            "var_key": request.var_key, "var_value": request.var_value, 
            "var_min": request.var_min, "var_max": request.var_max, "hpv":  request.highly_variable
            }
        )
    ads.adata_dic[ads.active_id] = adata      
    return adata


@pp_mcp.tool()
async def calculate_qc_metrics(request: CalculateQCMetrics, ctx: Context):
    """Calculate quality control metrics(common metrics: total counts, gene number, percentage of counts in ribosomal and mitochondrial) for AnnData."""
    result = await forward_request("pp_calculate_qc_metrics", request.model_dump())
    if result is not None:
        return result
    logger.info(f"calculate_qc_metrics {request.model_dump()}")
    func_kwargs = filter_args(request, sc.pp.calculate_qc_metrics)
    ads = ctx.request_context.lifespan_context
    adata = ads.adata_dic[ads.active_id]
    func_kwargs["inplace"] = True
    try:
        sc.pp.calculate_qc_metrics(adata, **func_kwargs)
        add_op_log(adata, sc.pp.calculate_qc_metrics, func_kwargs)
    except KeyError as e:
        raise KeyError(f"Cound find {e} in adata.var")
    except Exception as e:
        raise e
    return adata


@pp_mcp.tool()
async def log1p(request: Log1PModel, ctx: Context):
    """Logarithmize the data matrix (X = log(X + 1))"""
    result = await forward_request("pp_log1p", request.model_dump())
    if result is not None:
        return result
    func_kwargs = filter_args(request, sc.pp.log1p)
    ads = ctx.request_context.lifespan_context
    adata = ads.adata_dic[ads.active_id].copy()
    try:
        sc.pp.log1p(adata, **func_kwargs)
        adata.raw = adata.copy()
        add_op_log(adata, sc.pp.log1p, func_kwargs)
    except Exception as e:
        raise e
    ads.adata_dic[ads.active_id] = adata
    return adata


@pp_mcp.tool()
async def normalize_total(request: NormalizeTotalModel, ctx: Context):
    """Normalize counts per cell to the same total count"""
    result = await forward_request("pp_normalize_total", request.model_dump())
    if result is not None:
        return result
    func_kwargs = filter_args(request, sc.pp.normalize_total)
    ads = ctx.request_context.lifespan_context
    adata = ads.adata_dic[ads.active_id].copy()
    try:
        sc.pp.normalize_total(adata, **func_kwargs)
        add_op_log(adata, sc.pp.normalize_total, func_kwargs)
    except Exception as e:
        raise e
    ads.adata_dic[ads.active_id] = adata
    return adata


@pp_mcp.tool()
async def pca(request: PCAModel, ctx: Context):
    """Principal component analysis"""
    result = await forward_request("pp_pca", request.model_dump())
    if result is not None:
        return result
    func_kwargs = filter_args(request, sc.pp.pca)
    ads = ctx.request_context.lifespan_context
    adata = ads.adata_dic[ads.active_id]
    sc.pp.pca(adata, **func_kwargs)
    add_op_log(adata, sc.pp.pca, func_kwargs)
    return adata


@pp_mcp.tool()
async def highly_variable_genes(request: HighlyVariableGenesModel, ctx: Context):
    """Annotate highly variable genes"""
    result = await forward_request("pp_highly_variable_genes", request.model_dump())
    if result is not None:
        return result
    try:  
        func_kwargs = filter_args(request, sc.pp.highly_variable_genes)
        ads = ctx.request_context.lifespan_context
        adata = ads.adata_dic[ads.active_id]
        sc.pp.highly_variable_genes(adata, **func_kwargs)
        add_op_log(adata, sc.pp.highly_variable_genes, func_kwargs)
    except Exception as e:
        logger.error(f"Error in pp_highly_variable_genes: {str(e)}")
        raise e
    return adata


@pp_mcp.tool()
async def regress_out(request: RegressOutModel, ctx: Context):
    """Regress out (mostly) unwanted sources of variation."""
    result = await forward_request("pp_regress_out", request.model_dump())
    if result is not None:
        return result        
    func_kwargs = filter_args(request, sc.pp.regress_out)
    ads = ctx.request_context.lifespan_context
    adata = ads.adata_dic[ads.active_id].copy()
    try:
        sc.pp.regress_out(adata, **func_kwargs)
        add_op_log(adata, sc.pp.regress_out, func_kwargs)
    except Exception as e:
        raise e
    ads.adata_dic[ads.active_id] = adata
    return adata


@pp_mcp.tool()
async def scale(request: ScaleModel, ctx: Context):
    """Scale data to unit variance and zero mean"""
    result = await forward_request("pp_scale", request.model_dump())
    if result is not None:
        return result     
    func_kwargs = filter_args(request, sc.pp.scale)
    ads = ctx.request_context.lifespan_context
    adata = ads.adata_dic[ads.active_id].copy()
    try:
        sc.pp.scale(adata, **func_kwargs)
        add_op_log(adata, sc.pp.scale, func_kwargs)
    except Exception as e:
        raise e
    ads.adata_dic[ads.active_id] = adata        
    return adata


@pp_mcp.tool()
async def combat(request: CombatModel, ctx: Context):
    """ComBat function for batch effect correction"""
    result = await forward_request("pp_combat", request.model_dump())
    if result is not None:
        return result        
    func_kwargs = filter_args(request, sc.pp.combat)
    ads = ctx.request_context.lifespan_context
    adata = ads.adata_dic[ads.active_id].copy()
    try:
        sc.pp.combat(adata, **func_kwargs)
        add_op_log(adata, sc.pp.combat, func_kwargs)
    except Exception as e:
        raise e
    ads.adata_dic[ads.active_id] = adata         
    return adata


@pp_mcp.tool()
async def scrublet(request: ScrubletModel, ctx: Context):
    """Predict doublets using Scrublet"""
    result = await forward_request("pp_scrublet", request.model_dump())
    if result is not None:
        return result          
    func_kwargs = filter_args(request, sc.pp.scrublet)
    ads = ctx.request_context.lifespan_context
    adata = ads.adata_dic[ads.active_id]
    sc.pp.scrublet(adata, **func_kwargs)
    add_op_log(adata, sc.pp.scrublet, func_kwargs)
    return adata


@pp_mcp.tool()
async def neighbors(request: NeighborsModel, ctx: Context):
    """Compute nearest neighbors distance matrix and neighborhood graph"""
    result = await forward_request("pp_neighbors", request.model_dump())
    if result is not None:
        return result
    func_kwargs = filter_args(request, sc.pp.neighbors)
    ads = ctx.request_context.lifespan_context
    adata = ads.adata_dic[ads.active_id]
    sc.pp.neighbors(adata, **func_kwargs)
    add_op_log(adata, sc.pp.neighbors, func_kwargs)
    return adata
