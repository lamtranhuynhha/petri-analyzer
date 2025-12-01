"""
visualize.py
-------------
API endpoints cho visualization (Graphviz)
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from app.core.schemas import VisualizationRequest
from app.utils.graphviz_helper import (
    render_reachability_graph,
    render_coverability_tree,
    render_petri_net
)
import base64

router = APIRouter(prefix="/api/visualize", tags=["Visualization"])


@router.post("/reachability")
async def visualize_reachability(request: VisualizationRequest):
    """
    Generate visualization của Reachability Graph
    """
    try:
        rg_data = request.data
        format_type = request.format.lower()
        
        # Render với Graphviz
        image_data = render_reachability_graph(
            rg_data.get('states', []),
            rg_data.get('edges', []),
            rg_data.get('deadlocks', []),
            format_type
        )
        
        if format_type == 'svg':
            return Response(content=image_data, media_type="image/svg+xml")
        elif format_type == 'png':
            return Response(content=image_data, media_type="image/png")
        else:
            # Return base64 encoded
            encoded = base64.b64encode(image_data).decode()
            return {"image_data": f"data:image/{format_type};base64,{encoded}"}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error visualizing RG: {str(e)}")


@router.post("/coverability")
async def visualize_coverability(request: VisualizationRequest):
    """
    Generate visualization của Coverability Tree
    """
    try:
        tree_data = request.data
        format_type = request.format.lower()
        
        image_data = render_coverability_tree(
            tree_data.get('nodes', []),
            tree_data.get('edges', []),
            format_type
        )
        
        if format_type == 'svg':
            return Response(content=image_data, media_type="image/svg+xml")
        elif format_type == 'png':
            return Response(content=image_data, media_type="image/png")
        else:
            encoded = base64.b64encode(image_data).decode()
            return {"image_data": f"data:image/{format_type};base64,{encoded}"}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error visualizing coverability tree: {str(e)}")


@router.post("/petri-net")
async def visualize_petri_net(request: VisualizationRequest):
    """
    Generate visualization của Petri Net structure
    """
    try:
        net_data = request.data
        format_type = request.format.lower()
        
        image_data = render_petri_net(
            net_data.get('places', []),
            net_data.get('transitions', []),
            net_data.get('arcs', []),
            net_data.get('initial_marking', {}),
            format_type
        )
        
        if format_type == 'svg':
            return Response(content=image_data, media_type="image/svg+xml")
        elif format_type == 'png':
            return Response(content=image_data, media_type="image/png")
        else:
            encoded = base64.b64encode(image_data).decode()
            return {"image_data": f"data:image/{format_type};base64,{encoded}"}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error visualizing Petri Net: {str(e)}")


