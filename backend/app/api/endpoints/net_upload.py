"""
API endpoints cho upload, convert và export Petri Net files
"""

from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from app.core.schemas import (
    UploadFileResponse,
    ExportRequest,
    ConvertRequest,
    ErrorResponse
)
from app.utils.pnml_parser import parse_pnml, generate_pnml
from app.utils.json_converter import validate_petri_net_json
from app.utils.graphviz_helper import *
import json
import io
from typing import Dict, Any

router = APIRouter(prefix="/api/net", tags=["File Operations"])

@router.post("/upload", response_model=UploadFileResponse)
async def upload_petri_net(file: UploadFile = File(...)):
    """
    Upload PNML or JSON file và parse thành format chuẩn
    """
    try:
        content = await file.read()
        filename = file.filename or "unknown"
        
        # Determine format from extension
        if filename.endswith('.pnml') or filename.endswith('.xml'):
            # Parse PNML
            parsed_net = parse_pnml(content.decode('utf-8'))
            file_format = 'pnml'
        
        elif filename.endswith('.json'):
            # Parse JSON
            parsed_net = json.loads(content.decode('utf-8'))
            validate_petri_net_json(parsed_net)
            file_format = 'json'
        
        else:
            raise HTTPException(
                status_code=400,
                detail="Unsupported file format. Please upload .pnml or .json file."
            )
        
        return UploadFileResponse(
            status="success",
            message=f"File uploaded successfully: {filename}",
            data={
                "filename": filename,
                "format": file_format,
                "parsed_net": parsed_net
            }
        )
    
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON format: {str(e)}")
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error uploading file: {str(e)}")


@router.post("/convert")
async def convert_format(request: ConvertRequest):
    """
    Convert giữa PNML và JSON formats
    """
    try:
        if request.input_format == 'pnml' and request.output_format == 'json':
            # PNML → JSON
            if isinstance(request.data, dict):
                return {"status": "success", "converted_data": request.data}
            
            parsed = parse_pnml(request.data)
            return {"status": "success", "converted_data": parsed}
        
        elif request.input_format == 'json' and request.output_format == 'pnml':
            # JSON → PNML
            if isinstance(request.data, str):
                data_dict = json.loads(request.data)
            else:
                data_dict = request.data
            
            pnml_string = generate_pnml(data_dict)
            return {"status": "success", "converted_data": pnml_string}
        
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported conversion: {request.input_format} to {request.output_format}"
            )
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error converting format: {str(e)}")


@router.post("/export")
async def export_petri_net(request: ExportRequest):
    """
    Export Petri Net sang PNML hoặc JSON file
    """
    try:
        net_data = request.net_data
        format_type = request.format.lower()
        
        if format_type == 'json':
            # Export as JSON
            json_string = json.dumps(net_data, indent=2)
            return StreamingResponse(
                io.BytesIO(json_string.encode()),
                media_type="application/json",
                headers={"Content-Disposition": "attachment; filename=petri_net.json"}
            )
        
        elif format_type == 'pnml':
            # Export as PNML
            pnml_string = generate_pnml(net_data)
            return StreamingResponse(
                io.BytesIO(pnml_string.encode()),
                media_type="application/xml",
                headers={"Content-Disposition": "attachment; filename=petri_net.pnml"}
            )
        
        elif format_type in ('png','svg'):
            image_bytes = render_petri_net(net_data,format_type)
            return StreamingResponse(
                io.BytesIO(image_bytes),
                media_type=f"image/{format_type}",
                headers={"Content-Disposition": f"attachment; filename=petri_net.{format_type}"}
            )
        
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported export format: {format_type}"
            )
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error exporting: {str(e)}")


@router.get("/health")
def health_check():
    """
    Health check endpoint
    """
    return {
        "status": "ok",
        "message": "Petri Net Analyzer backend is running"
    }

