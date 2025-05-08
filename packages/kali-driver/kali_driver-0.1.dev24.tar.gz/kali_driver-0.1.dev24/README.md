Driver is [there](https://gitlab.cyberspike.top/aszl/diamond-shovel/al-1s/drivers/kali-driver)

the driver were basically done, and waiting for @huancun to setup docker on that server (notify me to do it instead if required)

## API usage

#### Import

```python
from al1s.drivers.kali import KaliManager, KaliContainer
```

that all of the components

#### Create a new container

1. You should create a global `KaliManager` by using `KaliManager(config={..})`, config definitions are available [here](https://docker-py.readthedocs.io/en/stable/client.html#docker.client.DockerClient)
2. Call `KaliManager#create_container`, it returns a tuple of internal uuid, and a usable `KaliContainer`
3. The container will be deleted after 24 hours of inactivity

#### Destroy the container explicitly

Call `KaliManager#destroy_container` with its internal uuid

#### Interact with the container

Use `KaliContainer#send_command` with raw command to send a line of command to the terminal of container. It should also support nested console such as `msfconsole` or prompted things

Use `KaliContainer#read_newlines` to read from container. The output already returned before will **NOT** be returned again.

Do not call `KaliContainer#destroy`, use method I've mentioned above.

#### Example

```python
    kali_manager = KaliManager(
        config={
            'base_url': 'unix:///var/run/docker.sock',
            'timeout': 123
        }
    )
    c1_id, c1 = kali_manager.create_container()

    c1.send_command('whoami')
    print(c1.read_newlines())

    kali_manager.destroy_container(c1_id)

```