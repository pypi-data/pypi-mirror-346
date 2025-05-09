from fastmcp import FastMCP, Context
import os
import scanpy as sc
from ..schema.tl import *
from ..util import filter_args, add_op_log, forward_request
from ..logging_config import setup_logger
logger = setup_logger(log_file=os.environ.get("SCANPYMCP_LOG_FILE", None))

tl_mcp = FastMCP("ScanpyMCP-TL-Server")


@tl_mcp.tool()
async def tsne(request: TSNEModel, ctx: Context):
    """t-distributed stochastic neighborhood embedding (t-SNE) for visualization"""
    result = await forward_request("tl_tsne", request.model_dump())
    if result is not None:
        return result
    func_kwargs = filter_args(request, sc.tl.tsne)
    ads = ctx.request_context.lifespan_context
    adata = ads.adata_dic[ads.active_id]
    sc.tl.tsne(adata, **func_kwargs)
    add_op_log(adata, sc.tl.tsne, func_kwargs)
    return adata

@tl_mcp.tool()
async def umap(request: UMAPModel, ctx: Context):
    """Uniform Manifold Approximation and Projection (UMAP) for visualization"""
    result = await forward_request("tl_umap", request.model_dump())
    if result is not None:
        return result
    func_kwargs = filter_args(request, sc.tl.umap)
    ads = ctx.request_context.lifespan_context
    adata = ads.adata_dic[ads.active_id]
    sc.tl.umap(adata, **func_kwargs)
    add_op_log(adata, sc.tl.umap, func_kwargs)
    return adata

@tl_mcp.tool()
async def draw_graph(request: DrawGraphModel, ctx: Context):
    """Force-directed graph drawing"""
    result = await forward_request("tl_draw_graph", request.model_dump())
    if result is not None:
        return result    
    func_kwargs = filter_args(request, sc.tl.draw_graph)
    ads = ctx.request_context.lifespan_context
    adata = ads.adata_dic[ads.active_id]
    sc.tl.draw_graph(adata, **func_kwargs)
    add_op_log(adata, sc.tl.draw_graph, func_kwargs)
    return adata

@tl_mcp.tool()
async def diffmap(request: DiffMapModel, ctx: Context):
    """Diffusion Maps for dimensionality reduction"""
    result = await forward_request("tl_diffmap", request.model_dump())
    if result is not None:
        return result    
    func_kwargs = filter_args(request, sc.tl.diffmap)
    ads = ctx.request_context.lifespan_context
    adata = ads.adata_dic[ads.active_id]
    sc.tl.diffmap(adata, **func_kwargs)
    adata.obsm["X_diffmap"] = adata.obsm["X_diffmap"][:,1:]
    add_op_log(adata, sc.tl.diffmap, func_kwargs)
    return adata

@tl_mcp.tool()
async def embedding_density(request: EmbeddingDensityModel, ctx: Context):
    """Calculate the density of cells in an embedding"""
    result = await forward_request("tl_embedding_density", request.model_dump())
    if result is not None:
        return result        
    func_kwargs = filter_args(request, sc.tl.embedding_density)
    ads = ctx.request_context.lifespan_context
    adata = ads.adata_dic[ads.active_id]
    sc.tl.embedding_density(adata, **func_kwargs)
    add_op_log(adata, sc.tl.embedding_density, func_kwargs)
    return adata

@tl_mcp.tool()
async def leiden(request: LeidenModel, ctx: Context):
    """Leiden clustering algorithm for community detection"""
    result = await forward_request("tl_leiden", request.model_dump())
    if result is not None:
        return result            
    func_kwargs = filter_args(request, sc.tl.leiden)
    ads = ctx.request_context.lifespan_context
    adata = ads.adata_dic[ads.active_id]
    sc.tl.leiden(adata, **func_kwargs)
    add_op_log(adata, sc.tl.leiden, func_kwargs)
    return adata

@tl_mcp.tool()
async def louvain(request: LouvainModel, ctx: Context):
    """Louvain clustering algorithm for community detection"""
    result = await forward_request("tl_louvain", request.model_dump())
    if result is not None:
        return result          
    func_kwargs = filter_args(request, sc.tl.louvain)
    ads = ctx.request_context.lifespan_context
    adata = ads.adata_dic[ads.active_id]
    sc.tl.louvain(adata, **func_kwargs)
    add_op_log(adata, sc.tl.louvain, func_kwargs)
    return adata

@tl_mcp.tool()
async def dendrogram(request: DendrogramModel, ctx: Context):
    """Hierarchical clustering dendrogram"""
    result = await forward_request("tl_dendrogram", request.model_dump())
    if result is not None:
        return result        
    func_kwargs = filter_args(request, sc.tl.dendrogram)
    ads = ctx.request_context.lifespan_context
    adata = ads.adata_dic[ads.active_id]
    sc.tl.dendrogram(adata, **func_kwargs)
    add_op_log(adata, sc.tl.dendrogram, func_kwargs)
    return adata

@tl_mcp.tool()
async def dpt(request: DPTModel, ctx: Context):
    """Diffusion Pseudotime (DPT) analysis"""
    result = await forward_request("tl_dpt", request.model_dump())
    if result is not None:
        return result          
    func_kwargs = filter_args(request, sc.tl.dpt)
    ads = ctx.request_context.lifespan_context
    adata = ads.adata_dic[ads.active_id]
    sc.tl.dpt(adata, **func_kwargs)
    add_op_log(adata, sc.tl.dpt, func_kwargs)
    return adata

@tl_mcp.tool()
async def paga(request: PAGAModel, ctx: Context):
    """Partition-based graph abstraction"""
    result = await forward_request("tl_paga", request.model_dump())
    if result is not None:
        return result         
    func_kwargs = filter_args(request, sc.tl.paga)
    ads = ctx.request_context.lifespan_context
    adata = ads.adata_dic[ads.active_id]
    sc.tl.paga(adata, **func_kwargs)
    add_op_log(adata, sc.tl.paga, func_kwargs)
    return adata

@tl_mcp.tool()
async def ingest(request: IngestModel, ctx: Context):
    """Map labels and embeddings from reference data to new data"""
    result = await forward_request("tl_ingest", request.model_dump())
    if result is not None:
        return result       
    func_kwargs = filter_args(request, sc.tl.ingest)
    ads = ctx.request_context.lifespan_context
    adata = ads.adata_dic[ads.active_id]
    sc.tl.ingest(adata, **func_kwargs)
    add_op_log(adata, sc.tl.ingest, func_kwargs)
    return adata

@tl_mcp.tool()
async def rank_genes_groups(request: RankGenesGroupsModel, ctx: Context):
    """Rank genes for characterizing groups, for differentially expressison analysis"""
    result = await forward_request("tl_rank_genes_groups", request.model_dump())
    if result is not None:
        return result         
    func_kwargs = filter_args(request, sc.tl.rank_genes_groups)
    ads = ctx.request_context.lifespan_context
    adata = ads.adata_dic[ads.active_id]
    sc.tl.rank_genes_groups(adata, **func_kwargs)
    add_op_log(adata, sc.tl.rank_genes_groups, func_kwargs)
    return adata

@tl_mcp.tool()
async def filter_rank_genes_groups(request: FilterRankGenesGroupsModel, ctx: Context):
    """Filter out genes based on fold change and fraction of genes"""
    result = await forward_request("tl_filter_rank_genes_groups", request.model_dump())
    if result is not None:
        return result          
    func_kwargs = filter_args(request, sc.tl.filter_rank_genes_groups)
    ads = ctx.request_context.lifespan_context
    adata = ads.adata_dic[ads.active_id]
    sc.tl.filter_rank_genes_groups(adata, **func_kwargs)
    add_op_log(adata, sc.tl.filter_rank_genes_groups, func_kwargs)
    return adata

@tl_mcp.tool()
async def marker_gene_overlap(request: MarkerGeneOverlapModel, ctx: Context):
    """Calculate overlap between data-derived marker genes and reference markers"""
    result = await forward_request("tl_marker_gene_overlap", request.model_dump())
    if result is not None:
        return result         
    func_kwargs = filter_args(request, sc.tl.marker_gene_overlap)
    ads = ctx.request_context.lifespan_context
    adata = ads.adata_dic[ads.active_id]
    sc.tl.marker_gene_overlap(adata, **func_kwargs)
    add_op_log(adata, sc.tl.marker_gene_overlap, func_kwargs)
    return adata

@tl_mcp.tool()
async def score_genes(request: ScoreGenesModel, ctx: Context):
    """Score a set of genes based on their average expression"""
    result = await forward_request("tl_score_genes", request.model_dump())
    if result is not None:
        return result       
    func_kwargs = filter_args(request, sc.tl.score_genes)
    ads = ctx.request_context.lifespan_context
    adata = ads.adata_dic[ads.active_id]
    sc.tl.score_genes(adata, **func_kwargs)
    add_op_log(adata, sc.tl.score_genes, func_kwargs)
    return adata

@tl_mcp.tool()
async def score_genes_cell_cycle(request: ScoreGenesCellCycleModel, ctx: Context):
    """Score cell cycle genes and assign cell cycle phases"""
    result = await forward_request("tl_score_genes_cell_cycle", request.model_dump())
    if result is not None:
        return result       
    func_kwargs = filter_args(request, sc.tl.score_genes_cell_cycle)
    ads = ctx.request_context.lifespan_context
    adata = ads.adata_dic[ads.active_id]
    sc.tl.score_genes_cell_cycle(adata, **func_kwargs)
    add_op_log(adata, sc.tl.score_genes_cell_cycle, func_kwargs)
    return adata