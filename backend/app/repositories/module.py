from backend.app.models.learning_strand import Module

from .base import BaseRepository


class ModuleRepository(BaseRepository[Module]):
    model = Module
