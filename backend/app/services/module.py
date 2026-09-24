from app.repositories.module import ModuleRepository


class ModuleService:
    def __init__(self, module_repo: ModuleRepository) -> None:
        self._module_repo = module_repo