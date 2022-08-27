import json
import signal

import psutil
from flask import Flask

carla_simulator_proc = None
carla_launch_script = ['/home/carla/CarlaUE4.sh', '-RenderOffScreen']

app = Flask(__name__)


def _carla_service_is_active():
    global carla_simulator_proc
    return carla_simulator_proc is not None and carla_simulator_proc.poll() is None


def _start_process():
    global carla_launch_script
    return psutil.Popen(carla_launch_script, shell=False)


def _stop_process(carla_proc):
    def kill_child_processes(parent_pid, sig=signal.SIGTERM):
        try:
            parent = psutil.Process(parent_pid)
        except psutil.NoSuchProcess:
            return
        children = parent.children(recursive=True)
        for process in children:
            app.logger.warning("====> " + str(process.pid))
            process.kill()
            process.wait()

    app.logger.warning("====> " + str(carla_proc.pid))
    kill_child_processes(carla_proc.pid)
    carla_proc.kill()
    carla_proc.wait()


@app.route("/reload_simulator")
def reload_simulator():
    global carla_simulator_proc
    if _carla_service_is_active():
        _stop_process(carla_simulator_proc)
    carla_simulator_proc = _start_process()
    res = {'result': True, 'pid': carla_simulator_proc.pid}
    return json.dumps(res)


@app.route("/finish_simulation")
def finish_simulation():
    global carla_simulator_proc
    app.logger.warning("====> " + str(_carla_service_is_active()))

    if _carla_service_is_active():
        _stop_process(carla_simulator_proc)
    res = {'result': True}
    return json.dumps(res)
