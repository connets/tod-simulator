import json
import signal

import psutil
import zerorpc
from time import sleep


class CarlaHandlerRPC:

    def __init__(self) -> None:
        self._carla_simulator_proc = None
        self._carla_launch_script = ['/home/carla/CarlaUE4.sh', '-RenderOffScreen']

    def _carla_service_is_active(self):
        return self._carla_simulator_proc is not None and self._carla_simulator_proc.poll() is None

    def _start_process(self):
        self._carla_simulator_proc = psutil.Popen(self._carla_launch_script, shell=False)
        print(self._carla_simulator_proc.pid)
        while self._carla_simulator_proc.children(recursive=True) == 0:
            ...

    def _stop_process(self):
        def kill_child_processes(parent_pid, sig=signal.SIGTERM):
            try:
                parent = psutil.Process(parent_pid)
            except psutil.NoSuchProcess:
                return
            children = parent.children(recursive=True)
            for process in children:
                # app.logger.warning("====> " + str(process.pid))
                process.terminate()
                process.wait()

        # app.logger.warning("====> " + str(carla_proc.pid))
        kill_child_processes(self._carla_simulator_proc.pid)
        self._carla_simulator_proc.terminate()
        self._carla_simulator_proc.wait()


    def reload_simulator(self):
        if self._carla_service_is_active():
            self._stop_process()
        self._start_process()
        res = {'result': True, 'pid': self._carla_simulator_proc.pid}
        # return json.dumps(res)
        return True

    def close_simulator(self):
        # app.logger.warning("====> " + str(_carla_service_is_active()))
        if self._carla_service_is_active():
            self._stop_process()
        res = {'result': True}
        # return json.dumps(res)
        return True


if __name__ == '__main__':
    s = zerorpc.Server(CarlaHandlerRPC())
    s.bind('tcp://0.0.0.0:4242')
    print('RPC server running')
    s.run()
