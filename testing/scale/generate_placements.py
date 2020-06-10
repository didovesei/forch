import logging
import os
import yaml


def generate_placements(switches, host_port_range, count):
    contents = {}
    placements = {'device_mac_placements': contents}
    current_count = 0
    mac_prefix = '02:00:00:00:00:'

    for switch in switches:
        for port in range(*host_port_range):
            if current_count == count:
                return placements

            current_count += 1

            placement = {
                'switch': switch,
                'port': port,
                'connected': True
            }

            mac = mac_prefix + f'{current_count:02x}'
            contents[mac] = placement

    return placements


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    SWITCHES = ['nz-kiwi-t2sw1', 'nz-kiwi-t2sw2', 'nz-kiwi-t2sw3']
    HOST_PORTS = (1, 47)
    MAC_COUNT = 100

    PLACEMENTS = generate_placements(SWITCHES, HOST_PORTS, MAC_COUNT)

    PLACEMENTS_FILE = os.path.join(os.getenv('FORCH_CONFIG_DIR'), 'placements.yaml')

    with open(PLACEMENTS_FILE, 'w') as file:
        yaml.dump(PLACEMENTS, file)

    logging.info('Wrote placements to %s', PLACEMENTS_FILE)
