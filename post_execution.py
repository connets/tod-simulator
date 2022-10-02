import os, re, sys
import shutil
import multiprocessing

filter_scavetool = """(module =~ "TODNetTown4.car.app[0]" AND (
    (name =~ instructionDelay:vector) OR
    (name =~ packetReceived:count) OR
    (name =~ "packetReceived:vector(packetBytes)") OR
    (name =~ packetReceivedDelay:vector) OR
    (name =~ statusUpdateInterval) OR
    (name =~ throughput:vector))) OR
(module =~ "TODNetTown4.car.cellularNic.nrPhy" AND (
    (name =~ averageCqiDl:vector) OR
    (name =~ averageCqiUl:vector) OR
    (name =~ servingCell:vector))) OR
(module =~ "TODNetTown4.server.app[*]" AND (
    (name =~ packetReceived:count) OR
    (name =~ "packetReceived:sum(packetBytes)") OR
    (name =~ "packetReceived:vector(packetBytes)") OR
    (name =~ packetReceivedDelay:vector) OR
    (name =~ throughput:vector) OR
    (name =~ typename))) OR
(module =~ "TODNetTown4.gnb*.cellularNic.mac" AND (
    (name =~ avgServedBlocksDl:vector) OR
    (name =~ avgServedBlocksUl:vector) OR
    (name =~ macDelayDl:vector)))"""


def on_creation_omnet_result_folder(result_folder, sim_name):
    scavetool_command = f"""
    (cd {result_folder} && 
    opp_scavetool x -F CSV-R -f '{filter_scavetool}' -o omnet_results.csv {sim_name}.sca {sim_name}.vec &&
    rm {sim_name}.*)
    """
    os.system(scavetool_command)


def on_creation_carla_result_folder(result_folder, sim_name):
    # print('CARLA:', result_folder)
    ...


if __name__ == '__main__':
    # Move files to results directory

    carla_results_parent_path = './tod_analysis/archimedes_results/past_simulations_25_09/carla/test_carla_omnet/'
    omnet_results_parent_path = './tod_analysis/archimedes_results/past_simulations_25_09/omnet/'
    final_results_path = './tod_analysis/archimedes_results/merged_simulations_test/'

    if not os.path.exists(final_results_path):
        os.makedirs(final_results_path)

    all_simulations_name = os.listdir(carla_results_parent_path)
    # print(all_simulations_name)

    interested_omnet_extensions_results = {'vec', 'vci', 'sca', 'out'}
    def export_simulation(sim_name):
        carla_sim_path = carla_results_parent_path + sim_name + '/'
        destination_path = final_results_path + sim_name + '/'
        carla_destination_sim_path = destination_path + 'carla/'
        shutil.copytree(carla_sim_path, carla_destination_sim_path)
        on_creation_carla_result_folder(carla_destination_sim_path, sim_name)

        omnet_destination_sim_path = destination_path + 'omnet/'
        os.makedirs(omnet_destination_sim_path)
        for ext in interested_omnet_extensions_results:
            omnet_file_to_move = f'{omnet_results_parent_path}{sim_name}.{ext}'
            shutil.copy(omnet_file_to_move, omnet_destination_sim_path)
        on_creation_omnet_result_folder(omnet_destination_sim_path, sim_name)


    with multiprocessing.Pool() as p:
        p.map(export_simulation, all_simulations_name)
    # for simulation_name in all_simulations_name:
    #     export_simulation(simulation_name)
