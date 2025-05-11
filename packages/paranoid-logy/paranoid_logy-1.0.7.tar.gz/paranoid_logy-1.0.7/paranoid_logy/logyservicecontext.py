from dataclasses import dataclass


@dataclass
class LogyServiceContext:

    id: str
    host_name: str
    port_number: int

    def __init__(self, settings):
        self.id = settings['id']
        self.host_name = settings['host']
        self.port_number = settings['portNumber']

    def get_endpoint(self) -> str:
        return 'http://{0}:{1}/messages'.format(self.host_name, self.port_number)
