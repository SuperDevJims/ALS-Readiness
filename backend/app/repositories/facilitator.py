from app.models.facilitator import Facilitator

from .base import BaseRepository


class FacilitatorRepository(BaseRepository[Facilitator]):

    model = Facilitator
