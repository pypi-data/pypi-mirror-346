import os
import threading
import time
import urllib
import uuid

import docker
from pwn import ssh


class KaliContainer:
    def __init__(self, uuid, owner, host):
        self._uuid = uuid
        self._owner = owner
        self._host = host

        self._container = owner._docker_client.containers.create(image="gitlab.cyberspike.top:5050/aszl/diamond-shovel/al-1s/kali-image:main", command="/usr/sbin/sshd -D", ports={"22/tcp": None}, detach=True)
        self._ssh_connection = None

    def _ensure_started(self):
        if self._container.status != "running":
            self._container.start()

    def _ensure_connected(self):
        self._ensure_started()

        if self._ssh_connection is None:
            self._container.reload()
            port_list = [x['PublicPort'] for x in self._container.ports if x['PrivatePort'] == 22 and x['Type'] == 'tcp']
            if len(port_list) != 1:
                raise Exception(f"Failed to find the port in port list {self._container.ports}")
            self._ssh_connection = ssh(user='root', host='localhost', keyfile=os.environ['HOME'] + '/.ssh/id_ecdsa', port=port_list[0])

    def send_command(self, command):
        self._ensure_started()

        # tty from docker is blocking so we decided to go with SSH
        self._ensure_connected()
        self._ssh_connection.sendline(command)
        self._owner._update_activity(self._uuid)

    def read_newlines(self):
        self._ensure_started()

        self._ensure_connected()
        self._owner._update_activity(self._uuid)

        result = ''
        while True:
            newline = self._ssh_connection.recvline(timeout=1)
            if newline == b'':
                break

            result += newline.decode('utf-8')
        return result

    def destroy(self):
        self._container.stop()
        self._container.remove()


class KaliManager:
    def __init__(self, config=None):
        if config is None:
            self._docker_client = docker.from_env()
        else:
            self._docker_client = docker.DockerClient(**config)

        url = self._docker_client.api.base_url
        if not url.startswith('unix://'):
            self._host = urllib.parse.urlparse(url).hostname
        else:
            self._host = 'localhost'

        self._containers = {}

        self._watchdog_thread = threading.Thread(target=self._watchdog, daemon=True)
        self._watchdog_thread.start()

    def create_container(self):
        container_uuid = uuid.uuid4()
        self._containers[container_uuid] = KaliContainer(container_uuid, self, self._host), {'last_activity': time.time()}

        return container_uuid, self.find_container(container_uuid)

    def find_container(self, container_uuid):
        return self._containers[container_uuid][0]

    def _update_activity(self, uuid):
        self._containers[uuid][1]['last_activity'] = time.time()

    def _watchdog(self):
        while True:
            for uuid, (container, data) in self._containers.items():
                if time.time() - data['last_activity'] > 60 * 60 * 24:
                    container.destroy()
                    del self._containers[uuid]

            time.sleep(10)

    def destroy_container(self, container_uuid):
        self._containers[container_uuid].destroy()
        del self._containers[container_uuid]
