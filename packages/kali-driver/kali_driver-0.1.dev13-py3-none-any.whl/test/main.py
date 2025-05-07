from al1s.drivers.kali import KaliManager

if __name__ == '__main__':
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
