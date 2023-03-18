import json
import sys
import zmq


def send_info(socket, t):
    socket.send(json.dumps(t).encode("utf-8"))


def receive_info(socket):
    message = socket.recv()
    json_data = json.loads(message.decode("utf-8"))
    if json_data['simulation_status'] != 0:
        sys.exit(0)
    return json_data


if __name__ == '__main__':
    refresh_status = 0.01
    simulation_step = 0.01


    def read_json(type_request):
        with open(f'API/{type_request}.json') as f:
            return json.load(f)


    init_configuration_json = read_json('init')

    interested_actor = init_configuration_json['moving_actors'][0]
    actor_id = interested_actor['actor_id']
    agent_id = interested_actor['actor_configuration']['agent_id']

    if len(sys.argv) >= 2:
        init_configuration_json['carla_configuration']['seed'] = int(sys.argv[1])
        init_configuration_json['run_id'] +=  f"#{init_configuration_json['carla_configuration']['seed']}"

    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://tod_simulator:5555")
    print("connected")

    send_info(socket, init_configuration_json)
    message = receive_info(socket)
    timestamp = message['initial_timestamp']
    limit_sim_time = 15

    while True:
        for _ in range(int(refresh_status / simulation_step)):
            timestamp += simulation_step
            req = read_json('simulation_step')
            req['timestamp'] = timestamp
            send_info(socket, req)
            message = receive_info(socket)
            if message['simulation_status'] != 0: break
        if message['simulation_status'] != 0: break

        req = read_json('actor_status_update')
        req['timestamp'] = timestamp
        send_info(socket, req)

        message = receive_info(socket)
        if message['simulation_status'] != 0: break
        status_id = message['user_defined']['status_id']

        req = read_json('compute_instruction')
        req['user_defined']['status_id'] = status_id
        req['timestamp'] = timestamp
        send_info(socket, req)

        message = receive_info(socket)
        if message['simulation_status'] != 0:
            break
        instruction_id = message['user_defined']['instruction_id']

        req = read_json('apply_instruction')
        req['user_defined']['instruction_id'] = instruction_id
        req['timestamp'] = timestamp
        send_info(socket, req)
        message = receive_info(socket)
        if message['simulation_status'] != 0:
            break
