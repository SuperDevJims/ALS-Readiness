from app.models.curriculum import Module

from .base import BaseRepository


class ModuleRepository(BaseRepository[Module]):
    model = Module
