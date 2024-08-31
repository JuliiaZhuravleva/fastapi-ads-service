from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from . import models, schemas
from fastapi import HTTPException


async def add_item(session: AsyncSession, item):
    session.add(item)
    try:
        await session.commit()
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    return item


async def get_advertisement(session: AsyncSession, advertisement_id: int):
    result = await session.execute(select(models.Advertisement).filter(models.Advertisement.id == advertisement_id))
    return result.scalar_one_or_none()


async def update_advertisement(session: AsyncSession, advertisement_id: int,
                               advertisement: schemas.AdvertisementUpdate):
    stmt = update(models.Advertisement).where(models.Advertisement.id == advertisement_id).values(
        **advertisement.dict(exclude_unset=True))
    result = await session.execute(stmt)
    await session.commit()
    if result.rowcount == 0:
        return None
    return await get_advertisement(session, advertisement_id)


async def delete_advertisement(session: AsyncSession, advertisement_id: int):
    stmt = delete(models.Advertisement).where(models.Advertisement.id == advertisement_id)
    result = await session.execute(stmt)
    await session.commit()
    if result.rowcount == 0:
        return None
    return {"status": "deleted"}


async def search_advertisements(session: AsyncSession, search_params: dict):
    query = select(models.Advertisement)
    if search_params.get("title"):
        query = query.filter(models.Advertisement.title.ilike(f"%{search_params['title']}%"))
    if search_params.get("description"):
        query = query.filter(models.Advertisement.description.ilike(f"%{search_params['description']}%"))
    if search_params.get("min_price"):
        query = query.filter(models.Advertisement.price >= search_params["min_price"])
    if search_params.get("max_price"):
        query = query.filter(models.Advertisement.price <= search_params["max_price"])
    if search_params.get("author"):
        query = query.filter(models.Advertisement.author.ilike(f"%{search_params['author']}%"))

    result = await session.execute(query)
    return result.scalars().all()
