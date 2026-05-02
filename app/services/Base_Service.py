from fastapi import HTTPException,status
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID


class Base_service:
    def __init__(self,model:SQLModel,session:AsyncSession):
        self.model=model
        self.session=session


    async def _get(self,id:UUID):

        return await self.session.get(self.model,id)

    async def _add(self,data:SQLModel):
        self.session.add(data)
        await self.session.commit()
        await self.session.refresh(data)
        return data

    async def _patch(self,data:SQLModel):
         return await self._add(data)

    async def _delete(self,data:SQLModel):
        if data is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
        await self.session.delete(data)
        await self.session.commit()
        
        
        

        

