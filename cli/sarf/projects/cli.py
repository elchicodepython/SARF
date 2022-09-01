from dependency_injector.wiring import Provide, inject

from ..containers import Container
from .base import Project
from ..shared.cli.crud import handle_cli_crud, CLICrudOperations
from ..shared.crud.simple_crud import SimpleCRUD


class ProjectsCliController:
    @inject
    def __init__(
        self,
        crud_handler: SimpleCRUD[Project] = Provide[Container.projects_crud],
    ):
        self._crud_handler = crud_handler

    def handle_request(self, args, stdin):
        cli_crud = CLICrudOperations[Project](
            Project, self._crud_handler, {"name": {}}
        )
        if not handle_cli_crud(cli_crud, args):
            # handle not simple crud operations
            pass
