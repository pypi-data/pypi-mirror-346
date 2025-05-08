from maleo_foundation.managers.client.base import ClientManager, ClientHTTPControllerManager, ClientControllerManagers, ClientControllers, ClientServices
from maleo_foundation.managers.service import ServiceManager

class MaleoClientManager(ClientManager):
    def __init__(
        self,
        key:str,
        name:str,
        url:str,
        service_manager:ServiceManager
    ):
        super().__init__(key, name, service_manager)
        self._url = url

    def _initialize_controllers(self) -> None:
        #* Initialize managers
        http_controller_manager = ClientHTTPControllerManager(url=self._url)
        self._controller_managers = ClientControllerManagers(http=http_controller_manager)
        #* Initialize controllers
        #! This initialied an empty controllers. Extend this function in the actual class to initialize all controllers.
        self._controllers = ClientControllers()

    @property
    def controllers(self) -> ClientControllers:
        return self._controllers

    async def dispose(self) -> None:
        self._logger.info("Disposing client manager")
        await self._controller_managers.http.dispose()
        self._logger.info("Client manager disposed successfully")