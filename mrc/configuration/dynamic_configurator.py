import json

from kazoo.client import KazooClient
from kazoo.recipe.watchers import DataWatch


class DynamicConfigurator:
    def __init__(self, znode_path, zookeeper_ip, zookeeper_port, set_external_identity=None):
        self.master_unit = None
        self.target_position = None
        self._identity = None
        self._znode_path = znode_path
        self._zk_ip = zookeeper_ip
        self._zk_port = zookeeper_port
        self._set_external_identity = set_external_identity
        self.zk_client = None
        self._watcher = None
        self._setup_watcher()

    def set_identity(self, identity):
        self._identity = identity
        if self._set_external_identity is not None:
            self._set_external_identity(self._identity)

    def _setup_watcher(self):
        if self.zk_client is not None:
            self.zk_client.close()
        self.zk_client = KazooClient(hosts='{}:{}'.format(self._zk_ip, self._zk_port))
        self.zk_client.start()
        DataWatch(client=self.zk_client, path=self._znode_path, func=self._update_conifg)

    def _update_conifg(self, data, stat):
        new_config = json.loads(data.decode("utf-8"))
        self.master_unit = new_config['master']
        self.target_position = new_config['position']
        self.set_identity(new_config['identity'])


c = DynamicConfigurator('/abc', '127.0.0.1', '2181')

while True:
    pass
