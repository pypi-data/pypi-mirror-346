from typing import List, Callable
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..utils.retry_decorator import db_retry

from ..db_context import DbContext
from ..dtos.proxy_config_dto import ProxyConfigDto

class ProxyConfigDao:
    def __init__(self):
        self.get_db_context: Callable[[], DbContext] = DbContext


    @db_retry()
    async def merge(self, proxy_configs_dto_list: List[ProxyConfigDto], *, session: AsyncSession) -> None:
        db_proxies = await session.execute(select(ProxyConfigDto)).scalars().all()

        input_proxies_set = {
            (p.proxy_ip, p.proxy_port, p.protocol): p for p in proxy_configs_dto_list
        }
        db_proxies_map = {
            (db_p.proxy_ip, db_p.proxy_port, db_p.protocol): db_p for db_p in db_proxies
        }

        to_create_proxy_configs = set(input_proxies_set.keys()) - set(db_proxies_map.keys())
        for to_create_proxy_config in to_create_proxy_configs:
            new_proxy_dto = input_proxies_set[to_create_proxy_config]
            session.add(ProxyConfigDto(
                proxy_ip=new_proxy_dto.proxy_ip,
                proxy_port=new_proxy_dto.proxy_port,
                proxy_user=new_proxy_dto.proxy_user,
                proxy_pass=new_proxy_dto.proxy_pass,
                protocol=new_proxy_dto.protocol,
                source=new_proxy_dto.source,
                deleted=False
            ))

        to_delete_proxy_configs = set(db_proxies_map.keys()) - set(input_proxies_set.keys())
        for to_delete_proxy_config in to_delete_proxy_configs:
            proxy_to_delete = db_proxies_map[to_delete_proxy_config]
            if not proxy_to_delete.deleted:
                proxy_to_delete.deleted = True
                session.add(proxy_to_delete)


    @db_retry()
    async def mark_as_deleted_by_id(self, proxy_id: int, *, session: AsyncSession) -> None:
        proxy_to_delete = await session.get(ProxyConfigDto, proxy_id)
        if proxy_to_delete and not proxy_to_delete.deleted:
            proxy_to_delete.deleted = True
            session.add(proxy_to_delete)


    @db_retry()
    async def get_proxy(self, *, session: AsyncSession) -> ProxyConfigDto | None:
        proxy = await session.execute(
            select(ProxyConfigDto)
            .where(ProxyConfigDto.deleted == False)
            .limit(1)
        )
        return proxy.scalars().first()

