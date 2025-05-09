import os
import inspect
from functools import partial
import scanpy as sc
from fastmcp import FastMCP, Context
from ..schema.pl import *
from pathlib import Path
from ..logging_config import setup_logger
from ..util import filter_args, set_fig_path, add_op_log,forward_request, obsm2adata
from ..logging_config import setup_logger
logger = setup_logger(log_file=os.environ.get("SCANPYMCP_LOG_FILE", None))

pl_mcp = FastMCP("ScanpyMCP-PL-Server")



@pl_mcp.tool()
async def pca(request: PCAModel, ctx: Context):
    """Scatter plot in PCA coordinates. default figure for PCA plot"""
    result = await forward_request("pl_pca", request.model_dump())
    if result is not None:
        return result
    func_kwargs = filter_args(request, sc.pl.pca)
    ads = ctx.request_context.lifespan_context
    adata = ads.adata_dic[ads.active_id]
    
    func_kwargs.pop("return_fig", True)
    func_kwargs["show"] = False
    func_kwargs["save"] = ".png"
    fig = sc.pl.pca(adata, **func_kwargs)
    fig_path = set_fig_path("pca", **func_kwargs)
    add_op_log(adata, sc.pl.pca, func_kwargs)
    return {"figpath": fig_path}


@pl_mcp.tool()
async def diffmap(request: DiffusionMapModel, ctx: Context):
    """Plot diffusion map embedding of cells."""
    result = await forward_request("pl_diffmap", request.model_dump())
    if result is not None:
        return result    
    func_kwargs = filter_args(request, sc.pl.diffmap)
    ads = ctx.request_context.lifespan_context
    adata = ads.adata_dic[ads.active_id]
    
    func_kwargs.pop("return_fig", True)
    func_kwargs["show"] = False
    func_kwargs["save"] = ".png"
    
    fig = sc.pl.diffmap(adata, **func_kwargs)
    fig_path = set_fig_path("diffmap", **func_kwargs)
    add_op_log(adata, sc.pl.diffmap, func_kwargs)
    return {"figpath": fig_path}


@pl_mcp.tool()
async def violin(request: ViolinModel, ctx: Context):
    """Plot violin plot of one or more variables."""
    result = await forward_request("pl_violin", request.model_dump())
    if result is not None:
        return result        
    func_kwargs = filter_args(request, sc.pl.violin)
    ads = ctx.request_context.lifespan_context
    adata = ads.adata_dic[ads.active_id]
    func_kwargs.pop("return_fig", True)
    func_kwargs["show"] = False
    func_kwargs["save"] = ".png"
    if request.use_obsm is not None:
        adata = obsm2adata(adata, request.use_obsm)
    fig = sc.pl.violin(adata, **func_kwargs)
    fig_path = set_fig_path("violin", **func_kwargs)
    add_op_log(adata, sc.pl.violin, func_kwargs)
    return {"figpath": fig_path}


@pl_mcp.tool()
async def stacked_violin(request: StackedViolinModel, ctx: Context):
    """Plot stacked violin plots. Makes a compact image composed of individual violin plots stacked on top of each other."""
    result = await forward_request("pl_stacked_violin", request.model_dump())
    if result is not None:
        return result           
    func_kwargs = filter_args(request, sc.pl.stacked_violin)
    ads = ctx.request_context.lifespan_context
    adata = ads.adata_dic[ads.active_id]
    
    func_kwargs.pop("return_fig", True)
    func_kwargs["show"] = False
    func_kwargs["save"] = ".png"
    
    fig = sc.pl.stacked_violin(adata, **func_kwargs)
    fig_path = set_fig_path("stacked_violin", **func_kwargs)
    add_op_log(adata, sc.pl.stacked_violin, func_kwargs)
    return {"figpath": fig_path}


@pl_mcp.tool()
async def heatmap(request: HeatmapModel, ctx: Context):
    """Heatmap of the expression values of genes."""
    result = await forward_request("pl_heatmap", request.model_dump())
    if result is not None:
        return result           
    func_kwargs = filter_args(request, sc.pl.heatmap)
    ads = ctx.request_context.lifespan_context
    adata = ads.adata_dic[ads.active_id]
    
    func_kwargs.pop("return_fig", True)
    func_kwargs["show"] = False
    func_kwargs["save"] = ".png"
    
    fig = sc.pl.heatmap(adata, **func_kwargs)
    fig_path = set_fig_path("heatmap", **func_kwargs)
    add_op_log(adata, sc.pl.heatmap, func_kwargs)
    return {"figpath": fig_path}


@pl_mcp.tool()
async def dotplot(request: DotplotModel, ctx: Context):
    """Plot dot plot of expression values per gene for each group."""
    result = await forward_request("pl_dotplot", request.model_dump())
    if result is not None:
        return result           
    func_kwargs = filter_args(request, sc.pl.dotplot)
    ads = ctx.request_context.lifespan_context
    adata = ads.adata_dic[ads.active_id]
    
    func_kwargs.pop("return_fig", True)
    func_kwargs["show"] = False
    func_kwargs["save"] = ".png"
    
    fig = sc.pl.dotplot(adata, **func_kwargs)
    fig_path = set_fig_path("dotplot", **func_kwargs)
    add_op_log(adata, sc.pl.dotplot, func_kwargs)
    return {"figpath": fig_path}


@pl_mcp.tool()
async def matrixplot(request: MatrixplotModel, ctx: Context):
    """matrixplot, Create a heatmap of the mean expression values per group of each var_names."""
    result = await forward_request("pl_matrixplot", request.model_dump())
    if result is not None:
        return result
    func_kwargs = filter_args(request, sc.pl.matrixplot)
    ads = ctx.request_context.lifespan_context
    adata = ads.adata_dic[ads.active_id]
    
    func_kwargs.pop("return_fig", True)
    func_kwargs["show"] = False
    func_kwargs["save"] = ".png"
    if request.use_obsm is not None:
        adata = obsm2adata(adata, request.use_obsm)
    fig = sc.pl.matrixplot(adata, **func_kwargs)
    fig_path = set_fig_path("matrixplot", **func_kwargs)
    add_op_log(adata, sc.pl.matrixplot, func_kwargs)
    return {"figpath": fig_path}


@pl_mcp.tool()
async def tracksplot(request: TracksplotModel, ctx: Context):
    """tracksplot, compact plot of expression of a list of genes."""
    result = await forward_request("pl_tracksplot", request.model_dump())
    if result is not None:
        return result
    func_kwargs = filter_args(request, sc.pl.tracksplot)
    ads = ctx.request_context.lifespan_context
    adata = ads.adata_dic[ads.active_id]
    
    func_kwargs.pop("return_fig", True)
    func_kwargs["show"] = False
    func_kwargs["save"] = ".png"
    
    fig = sc.pl.tracksplot(adata, **func_kwargs)
    fig_path = set_fig_path("tracksplot", **func_kwargs)
    add_op_log(adata, sc.pl.tracksplot, func_kwargs)
    return {"figpath": fig_path}


@pl_mcp.tool()
async def scatter(request: EnhancedScatterModel, ctx: Context):
    """Plot a scatter plot of two variables, Scatter plot along observations or variables axes."""
    result = await forward_request("pl_scatter", request.model_dump())
    if result is not None:
        return result    
    func_kwargs = filter_args(request, sc.pl.scatter)
    ads = ctx.request_context.lifespan_context
    adata = ads.adata_dic[ads.active_id]
    
    func_kwargs.pop("return_fig", True)
    func_kwargs["show"] = False
    func_kwargs["save"] = ".png"
    
    fig = sc.pl.scatter(adata, **func_kwargs)
    fig_path = set_fig_path("scatter", **func_kwargs)
    add_op_log(adata, sc.pl.scatter, func_kwargs)
    return {"figpath": fig_path}


@pl_mcp.tool()
async def embedding(request: EmbeddingModel, ctx: Context):
    """Scatter plot for user specified embedding basis (e.g. umap, tsne, etc)."""
    result = await forward_request("pl_embedding", request.model_dump())
    if result is not None:
        return result       
    func_kwargs = filter_args(request, sc.pl.embedding)
    ads = ctx.request_context.lifespan_context
    adata = ads.adata_dic[ads.active_id]
    
    func_kwargs.pop("return_fig", True)
    func_kwargs["show"] = False
    func_kwargs["save"] = ".png"
    if request.use_obsm is not None:
        adata = obsm2adata(adata, request.use_obsm)
    try:      
        fig = sc.pl.embedding(adata, **func_kwargs)
    except KeyError as e:
        if request.use_obsm is None:
            raise KeyError(f"Key '{e}' not found in adata.var and adata.obs")
        else:
            raise KeyError(f"Key '{e}' not found in adata.obsm")
    except Exception as e:
        raise e
    fig_path = set_fig_path("embedding", **func_kwargs)
    add_op_log(adata, sc.pl.embedding, func_kwargs)
    return {"figpath": fig_path}


@pl_mcp.tool()
async def embedding_density(request: EmbeddingDensityModel, ctx: Context):
    """Plot the density of cells in an embedding."""
    result = await forward_request("pl_embedding_density", request.model_dump())
    if result is not None:
        return result          
    func_kwargs = filter_args(request, sc.pl.embedding_density)
    ads = ctx.request_context.lifespan_context
    adata = ads.adata_dic[ads.active_id]
    
    func_kwargs.pop("return_fig", True)
    func_kwargs["show"] = False
    func_kwargs["save"] = ".png"
    
    fig = sc.pl.embedding_density(adata, **func_kwargs)
    fig_path = set_fig_path("embedding_density", **func_kwargs)
    add_op_log(adata, sc.pl.embedding_density, func_kwargs)
    return {"figpath": fig_path}


@pl_mcp.tool()
async def rank_genes_groups(request: RankGenesGroupsModel, ctx: Context):
    """Plot ranking of genes based on differential expression."""
    result = await forward_request("pl_rank_genes_groups", request.model_dump())
    if result is not None:
        return result         
    func_kwargs = filter_args(request, sc.pl.rank_genes_groups)
    ads = ctx.request_context.lifespan_context
    adata = ads.adata_dic[ads.active_id]
    
    func_kwargs.pop("return_fig", True)
    func_kwargs["show"] = False
    func_kwargs["save"] = ".png"
    
    fig = sc.pl.rank_genes_groups(adata, **func_kwargs)
    fig_path = set_fig_path("rank_genes_groups", **func_kwargs)
    add_op_log(adata, sc.pl.rank_genes_groups, func_kwargs)
    return {"figpath": fig_path}


@pl_mcp.tool()
async def rank_genes_groups_dotplot(request: RankGenesGroupsDotplotModel, ctx: Context):
    """Plot ranking of genes(DEGs) using dotplot visualization. Defualt plot DEGs for rank_genes_groups tool"""
    result = await forward_request("pl_rank_genes_groups_dotplot", request.model_dump())
    if result is not None:
        return result
    func_kwargs = filter_args(request, sc.pl.rank_genes_groups_dotplot)
    ads = ctx.request_context.lifespan_context
    adata = ads.adata_dic[ads.active_id]
    
    func_kwargs.pop("return_fig", True)
    func_kwargs["show"] = False
    func_kwargs["save"] = ".png"
    
    fig = sc.pl.rank_genes_groups_dotplot(adata, **func_kwargs)
    fig_path = set_fig_path("rank_genes_groups_dotplot", **func_kwargs)
    add_op_log(adata, sc.pl.rank_genes_groups_dotplot, func_kwargs)
    return {"figpath": fig_path}


@pl_mcp.tool()
async def clustermap(request: ClusterMapModel, ctx: Context):
    """Plot hierarchical clustering of cells and genes."""
    result = await forward_request("pl_clustermap", request.model_dump())
    if result is not None:
        return result
    func_kwargs = filter_args(request, sc.pl.clustermap)
    ads = ctx.request_context.lifespan_context
    adata = ads.adata_dic[ads.active_id]
    
    func_kwargs.pop("return_fig", True)
    func_kwargs["show"] = False
    func_kwargs["save"] = ".png"
    
    fig = sc.pl.clustermap(adata, **func_kwargs)
    fig_path = set_fig_path("clustermap", **func_kwargs)
    add_op_log(adata, sc.pl.clustermap, func_kwargs)
    return {"figpath": fig_path}


@pl_mcp.tool()
async def highly_variable_genes(request: HighlyVariableGenesModel, ctx: Context):
    """plot highly variable genes; Plot dispersions or normalized variance versus means for genes."""
    result = await forward_request("pl_highly_variable_genes", request.model_dump())
    if result is not None:
        return result
    func_kwargs = filter_args(request, sc.pl.highly_variable_genes)
    ads = ctx.request_context.lifespan_context
    adata = ads.adata_dic[ads.active_id]
    
    func_kwargs.pop("return_fig", True)
    func_kwargs["show"] = False
    func_kwargs["save"] = ".png"
    
    fig = sc.pl.highly_variable_genes(adata, **func_kwargs)
    fig_path = set_fig_path("highly_variable_genes", **func_kwargs)
    add_op_log(adata, sc.pl.highly_variable_genes, func_kwargs)
    return {"figpath": fig_path}


@pl_mcp.tool()
async def pca_variance_ratio(request: PCAVarianceRatioModel, ctx: Context):
    """Plot the PCA variance ratio to visualize explained variance."""
    result = await forward_request("pl_pca_variance_ratio", request.model_dump())
    if result is not None:
        return result
    func_kwargs = filter_args(request, sc.pl.pca_variance_ratio)
    ads = ctx.request_context.lifespan_context
    adata = ads.adata_dic[ads.active_id]
    
    func_kwargs.pop("return_fig", True)
    func_kwargs["show"] = False
    func_kwargs["save"] = ".png"
    
    fig = sc.pl.pca_variance_ratio(adata, **func_kwargs)
    fig_path = set_fig_path("pca_variance_ratio", **func_kwargs)
    add_op_log(adata, sc.pl.pca_variance_ratio, func_kwargs)
    return {"figpath": fig_path}

