from app.models.module import Module

from .base import BaseRepository


class ModuleRepository(BaseRepository[Module]):
    model = Module
