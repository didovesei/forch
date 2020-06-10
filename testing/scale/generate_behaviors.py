import logging
import os
import random
import yaml


def generate_random_behaviors(segments, roles, count):
    contents = {}
    behaviors = {'device_mac_behaviors': contents}
    mac_prefix = '02:00:00:00:00:'

    for current_count in range(1, count+1):
        mac = mac_prefix + f'{current_count:02x}'
        segment = random.choice(segments)
        role = random.choice(roles)
        behavior = {
            'segment': segment,
            'role': role
        }
        contents[mac] = behavior

    return behaviors


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    SEGMENTS = ['INFRA', 'BOS']
    ROLES = ['red', 'green', 'blue']

    BEHAVIORS = generate_random_behaviors(SEGMENTS, ROLES, 100)

    BEHAVIORS_FILE = os.path.join(os.getenv('FORCH_CONFIG_DIR'), 'behaviors.yaml')

    with open(BEHAVIORS_FILE, 'w') as file:
        yaml.dump(BEHAVIORS, file)

    logging.info('Wrote behaviors to %s', BEHAVIORS_FILE)
