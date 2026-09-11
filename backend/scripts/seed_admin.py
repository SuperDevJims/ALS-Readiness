# This script is for creating an admin account.
# Run 'uv run python -m backend.scripts.seed_admin'.
# Credentials should be printed in the terminal.

import asyncio
import sys

from sqlalchemy.ext.asyncio import AsyncSession

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from app.db.session import AsyncSessionLocal
from app.enums.user import UserRole
from app.models.user import User

from .seed_user import create_user


async def create_admin(session: AsyncSession) -> User:
    return await create_user(UserRole.ADMIN, session)


async def main() -> None:
    async with AsyncSessionLocal() as session, session.begin():
        await create_admin(session)


if __name__ == "__main__":
    asyncio.run(main())
