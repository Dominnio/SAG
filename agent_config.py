server_name = 'protonxmpp.ch'

agent_1 = { #detects - dogs
    'jjd': 'spade_pro1@{}'.format(server_name),
    'password': '1qwerty8',
    'hostname': '127.0.0.1',
    'port': '10001',
    'training_set_path': 'C:\\DEV\\PycharmProjects\\SAG_agents\\datasets\\dogs\\training_set',
    'test_set_path': 'C:\\DEV\\PycharmProjects\\SAG_agents\\datasets\\dogs\\test_set',
    'steps_per_epoch': '10',
    'epochs': '1',
    'validation_steps': '10'
}

agent_2 = { #detects - cats
    'jjd': 'spade_pro2@{}'.format(server_name),
    'password': '2qwerty8',
    'hostname': '127.0.0.1',
    'port': '10002',
    'training_set_path': 'C:\\DEV\\PycharmProjects\\SAG_agents\\datasets\\cats\\training_set',
    'test_set_path': 'C:\\DEV\\PycharmProjects\\SAG_agents\\datasets\\cats\\test_set',
    'steps_per_epoch': '10',
    'epochs': '1',
    'validation_steps': '10'
}

agent_3 = { #detects - horses
    'jjd': 'spade_pro3@{}'.format(server_name),
    'password': '3qwerty8',
    'hostname': '127.0.0.1',
    'port': '10003',
    'training_set_path': 'C:\\DEV\\PycharmProjects\\SAG_agents\\datasets\\horses\\training_set',
    'test_set_path': 'C:\\DEV\\PycharmProjects\\SAG_agents\\datasets\\horses\\test_set',
    'steps_per_epoch': '10',
    'epochs': '1',
    'validation_steps': '10'
}

agent_4 = { #detects - chickens
    'jjd': 'spade_pro4@{}'.format(server_name),
    'password': '4qwerty8',
    'hostname': '127.0.0.1',
    'port': '10004',
    'training_set_path': 'C:\\DEV\\PycharmProjects\\SAG_agents\\datasets\\chickens\\training_set',
    'test_set_path': 'C:\\DEV\\PycharmProjects\\SAG_agents\\datasets\\chickens\\test_set',
    'steps_per_epoch': '10',
    'epochs': '1',
    'validation_steps': '10'
}

agent_5 = { #not used
    'jjd': 'spade_pro5@{}'.format(server_name),
    'password': '5qwerty8',
    'hostname': '127.0.0.1',
    'port': '10005'
}

agent_0 = { # not used
    'jjd': 'spade_pro@{}'.format(server_name),
    'password': '6qwerty8',
    'hostname': '127.0.0.1',
    'port': '10000'
}

test_images = {
    'cat1': 'C:\\DEV\\PycharmProjects\\SAG_agents\\datasets\\single_prediction\\cat.1.jpg',
    'cat2': 'C:\\DEV\\PycharmProjects\\SAG_agents\\datasets\\single_prediction\\cat.2.jpg',
    'chicken1': 'C:\\DEV\\PycharmProjects\\SAG_agents\\datasets\\single_prediction\\chicken.1.jpeg',
    'chicken2': 'C:\\DEV\\PycharmProjects\\SAG_agents\\datasets\\single_prediction\\chicken.2.jpeg',
    'dog1': 'C:\\DEV\\PycharmProjects\\SAG_agents\\datasets\\single_prediction\\dog.1.jpg',
    'dog2': 'C:\\DEV\\PycharmProjects\\SAG_agents\\datasets\\single_prediction\\dog.2.jpg',
    'horse1': 'C:\\DEV\\PycharmProjects\\SAG_agents\\datasets\\single_prediction\\horse.1.jpeg',
    'horse2': 'C:\\DEV\\PycharmProjects\\SAG_agents\\datasets\\single_prediction\\horse.2.jpeg'
}