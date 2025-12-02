from fastapi import APIRouter, Depends, Query, HTTPException
from typing import List, Optional
from datetime import datetime
import pandas as pd
from app.dependencies import get_api_key
from app.services.data_loader import data_loader

router = APIRouter(dependencies=[Depends(get_api_key)])

@router.get("/clases")
async def get_clases(
    fecha_inicio: Optional[datetime] = None,
    fecha_fin: Optional[datetime] = None,
    profesor: Optional[str] = None,
    mes: Optional[str] = None, # Expecting format like '2023-11' or just '11'
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=1000)
):
    df = data_loader.get_data()
    
    if df.empty:
        return {"success": True, "data": [], "meta": {"total": 0, "page": page, "limit": limit}}

    # Filtering
    if fecha_inicio:
        df = df[df['Start Time'] >= fecha_inicio]
    if fecha_fin:
        df = df[df['Start Time'] <= fecha_fin]
    if profesor:
        # Case insensitive partial match
        df = df[df['User Name'].str.contains(profesor, case=False, na=False) | 
                df['User Email'].str.contains(profesor, case=False, na=False)]
    if mes:
        # Assuming mes is numeric month '11' or '2023-11'
        # If '2023-11', we can convert to string and check startswith
        # If '11', we check month attribute
        try:
            if '-' in mes:
                df = df[df['Start Time'].dt.strftime('%Y-%m') == mes]
            else:
                df = df[df['Start Time'].dt.month == int(mes)]
        except Exception:
            pass # Ignore invalid month filter

    total = len(df)
    
    # Pagination
    start = (page - 1) * limit
    end = start + limit
    
    paginated_df = df.iloc[start:end]
    
    # Convert to dict, handling NaNs
    data = paginated_df.where(pd.notnull(paginated_df), None).to_dict(orient='records')
    
    return {
        "success": True,
        "data": data,
        "meta": {
            "total": total,
            "page": page,
            "limit": limit,
            "timestamp": datetime.now().isoformat()
        }
    }

@router.get("/clases/{id}")
async def get_clase(id: str):
    df = data_loader.get_data()
    if df.empty:
        raise HTTPException(status_code=404, detail="Class not found")
        
    # Assuming 'Meeting ID' is the ID, but it might not be unique per session.
    # If we treat 'Meeting ID' as the ID:
    # We need to handle type (int vs str)
    
    # Try to match as string
    match = df[df['Meeting ID'].astype(str) == id]
    
    if match.empty:
        raise HTTPException(status_code=404, detail="Class not found")
        
    # Return the first match or all matches? Requirement says "individual class object"
    # If multiple exist (recurring meeting), we might need a better ID strategy.
    # For now, return the first one.
    record = match.iloc[0].where(pd.notnull(match.iloc[0]), None).to_dict()
    return {"success": True, "data": record}

@router.get("/estadisticas")
async def get_estadisticas(
    fecha_inicio: Optional[datetime] = None,
    fecha_fin: Optional[datetime] = None
):
    df = data_loader.get_data()
    if df.empty:
        return {"success": True, "data": {}}

    if fecha_inicio:
        df = df[df['Start Time'] >= fecha_inicio]
    if fecha_fin:
        df = df[df['Start Time'] <= fecha_fin]

    total_clases = len(df)
    avg_duration = df['Duration (Minutes)'].mean() if 'Duration (Minutes)' in df.columns else 0
    total_participants = df['Participants'].sum() if 'Participants' in df.columns else 0
    
    return {
        "success": True,
        "data": {
            "total_clases": total_clases,
            "promedio_duracion_minutos": round(avg_duration, 2),
            "total_participantes": int(total_participants)
        }
    }

@router.get("/profesores")
async def get_profesores():
    df = data_loader.get_data()
    if df.empty:
        return {"success": True, "data": []}
        
    profesores = []
    if 'User Name' in df.columns:
        profesores = df['User Name'].dropna().unique().tolist()
        
    return {"success": True, "data": sorted(profesores)}

@router.get("/health")
async def health_check():
    last_updated = data_loader.get_last_updated()
    return {
        "status": "ok",
        "last_data_update": last_updated.isoformat() if last_updated else None
    }
