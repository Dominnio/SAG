import os

server_name = 'jabber.hot-chilli.net'

agents_dict = {
    'agent_1': { #detects - dogs
        'jid': 'spade_pro1@{}'.format(server_name),
        'password': '1qwerty8',
        'hostname': '127.0.0.1',
        'port': '10001',
        'training_set_path': os.path.join('..', 'datasets', 'dogs', 'training_set'),
        'test_set_path': os.path.join('..', 'datasets', 'dogs', 'test_set'),
        'purpose': 'dogs',
        'steps_per_epoch': '1',
        'epochs': '1',
        'validation_steps': '1'
    },
    'agent_2': { #detects - cats
        'jid': 'spade_pro2@{}'.format(server_name),
        'password': '1qwerty8',
        'hostname': '127.0.0.1',
        'port': '10002',
        'training_set_path': os.path.join('..', 'datasets', 'cats', 'training_set'),
        'test_set_path': os.path.join('..', 'datasets', 'cats', 'test_set'),
        'purpose': 'cats',
        'steps_per_epoch': '1',
        'epochs': '1',
        'validation_steps': '1'
    },
      'agent_3': { #detects - horses
        'jid': 'spade_pro3@{}'.format(server_name),
        'password': '1qwerty8',
        'hostname': '127.0.0.1',
        'port': '10003',
        'training_set_path': os.path.join('..', 'datasets', 'horses', 'training_set'),
        'test_set_path': os.path.join('..', 'datasets', 'horses', 'test_set'),
        'purpose': 'horses',
        'steps_per_epoch': '1',
        'epochs': '1',
        'validation_steps': '1'
      },
    'agent_4': { #detects - chickens
        'jid': 'spade_pro4@{}'.format(server_name),
        'password': '1qwerty8',
        'hostname': '127.0.0.1',
        'port': '10004',
        'training_set_path': os.path.join('..', 'datasets', 'chickens', 'training_set'),
        'test_set_path': os.path.join('..', 'datasets', 'chickens', 'test_set'),
        'purpose': 'chickens',
        'steps_per_epoch': '1',
        'epochs': '1',
        'validation_steps': '1'
    }
}

test_images = {
    'cat1': os.path.join('..', 'datasets', 'single_prediction', 'cat.1.jpg'),
    'cat2': os.path.join('..', 'datasets', 'single_prediction', 'cat.2.jpg'),
    'chicken1': os.path.join('..', 'datasets', 'single_prediction', 'chicken.1.jpeg'),
    'chicken2': os.path.join('..', 'datasets', 'single_prediction', 'chicken.2.jpeg'),
    'dog1': os.path.join('..', 'datasets', 'single_prediction', 'dog.1.jpg'),
    'dog2': os.path.join('..', 'datasets', 'single_prediction', 'dog.2.jpg'),
    'horse1': os.path.join('..', 'datasets', 'single_prediction', 'horse.1.jpeg'),
    'horse2': os.path.join('..', 'datasets', 'single_prediction', 'horse.2.jpeg')
}