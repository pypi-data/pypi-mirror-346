import pydantic
from sqlalchemy.ext.asyncio import (
    async_sessionmaker as sqlalchemy_async_sessionmaker,
    AsyncEngine as SQLAlchemyAsyncEngine,
    AsyncSession as SQLAlchemyAsyncSession,
    create_async_engine as create_sqlalchemy_async_engine,
)
from sqlalchemy.pool import Pool as SQLAlchemyPool, QueuePool as SQLAlchemyQueuePool

from src.config.manager import settings


class AsyncDatabase:
    def __init__(self):
        self.mysql_uri: str = (
            f"mysql+aiomysql://{settings.DB_MYSQL_USERNAME}:{settings.DB_MYSQL_PASSWORD}"
            f"@{settings.DB_MYSQL_HOST}:{settings.DB_MYSQL_PORT}/{settings.DB_MYSQL_NAME}"
        )
        self.async_engine: SQLAlchemyAsyncEngine = create_sqlalchemy_async_engine(
            url=self.mysql_uri,
            echo=settings.IS_DB_ECHO_LOG,
            pool_size=settings.DB_POOL_SIZE,
            max_overflow=settings.DB_POOL_OVERFLOW,
            # 注意：异步引擎不能使用QueuePool
            # MySQL特定参数
            pool_pre_ping=True,  # 连接健康检查
            pool_recycle=3600,   # 连接回收时间(秒)
        )
        self.pool: SQLAlchemyPool = self.async_engine.pool
        self.async_session_maker = sqlalchemy_async_sessionmaker(
            bind=self.async_engine, 
            class_=SQLAlchemyAsyncSession, 
            expire_on_commit=settings.IS_DB_EXPIRE_ON_COMMIT
        )


async_db: AsyncDatabase = AsyncDatabase()
