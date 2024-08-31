from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from . import crud, models, schemas
from .database import engine, get_session

app = FastAPI()


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)


@app.post("/advertisement", response_model=schemas.Advertisement)
async def create_advertisement(advertisement: schemas.AdvertisementCreate, session: AsyncSession = Depends(get_session)):
    db_advertisement = models.Advertisement(**advertisement.dict())
    return await crud.add_item(session=session, item=db_advertisement)


@app.get("/advertisement/{advertisement_id}", response_model=schemas.Advertisement)
async def read_advertisement(advertisement_id: int, session: AsyncSession = Depends(get_session)):
    db_advertisement = await crud.get_advertisement(session, advertisement_id=advertisement_id)
    if db_advertisement is None:
        raise HTTPException(status_code=404, detail="Advertisement not found")
    return db_advertisement


@app.patch("/advertisement/{advertisement_id}", response_model=schemas.Advertisement)
async def update_advertisement(advertisement_id: int, advertisement: schemas.AdvertisementUpdate, session: AsyncSession = Depends(get_session)):
    db_advertisement = await crud.update_advertisement(session, advertisement_id=advertisement_id, advertisement=advertisement)
    if db_advertisement is None:
        raise HTTPException(status_code=404, detail="Advertisement not found")
    return db_advertisement


@app.delete("/advertisement/{advertisement_id}", response_model=dict)
async def delete_advertisement(advertisement_id: int, session: AsyncSession = Depends(get_session)):
    result = await crud.delete_advertisement(session, advertisement_id=advertisement_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Advertisement not found")
    return result


@app.get("/advertisement", response_model=List[schemas.Advertisement])
async def search_advertisements(
    title: Optional[str] = Query(None, description="Search by title"),
    description: Optional[str] = Query(None, description="Search by description"),
    min_price: Optional[float] = Query(None, description="Minimum price"),
    max_price: Optional[float] = Query(None, description="Maximum price"),
    author: Optional[str] = Query(None, description="Search by author"),
    session: AsyncSession = Depends(get_session)
):
    search_params = {
        "title": title,
        "description": description,
        "min_price": min_price,
        "max_price": max_price,
        "author": author
    }
    return await crud.search_advertisements(session, search_params)
