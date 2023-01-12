import os, glob
import shutil
import multiprocessing
import subprocess

filters_scavetool = {
    "car": """(module =~ "TODNetTown4.car.app[0]" AND (
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

        (module =~ "TODNetTown4.car.cellularNic.nrMac" AND (
        (name =~ harqErrorRate_1st_Dl:vector) OR
        (name =~ harqErrorRate_2nd_Dl:vector) OR
        (name =~ harqErrorRate_2nd_Ul:vector) OR
        (name =~ harqErrorRate_3rd_Ul:vector) OR
        (name =~ harqErrorRate_4th_Ul:vector) OR
        (name =~ harqErrorRateDl:vector) OR
        (name =~ harqErrorRateUl:vector) OR
        (name =~ harqTxAttemptsDl:vector) OR
        (name =~ harqTxAttemptsUl:vector) OR
        (name =~ macDelayUl:vector)))""",
    "server": """(module =~ "TODNetTown4.server.app[*]" AND (
        (name =~ packetReceived:count) OR
        (name =~ "packetReceived:sum(packetBytes)") OR
        (name =~ "packetReceived:vector(packetBytes)") OR
        (name =~ packetReceivedDelay:vector) OR
        (name =~ throughput:vector) OR
        (name =~ typename)))""",
    "gnb": """(module =~ "TODNetTown4.gnb*.cellularNic.mac" AND (
        (name =~ avgServedBlocksDl:vector) OR
        (name =~ avgServedBlocksUl:vector) OR
        (name =~ macDelayDl:vector)))"""
}


def on_creation_omnet_result_folder(result_folder, sim_name):
    global filters_scavetool

    for name in filters_scavetool.keys():
        scavetool_command = f"""opp_scavetool x -F CSV-R -f '{filters_scavetool[name]}' -o {name}.csv {sim_name}.sca {sim_name}.vec"""
        p = subprocess.Popen(['opp_scavetool', 'x', '-F', 'CSV-R', '-f', filters_scavetool[name], '-o', f'{name}.csv', f'{sim_name}.sca', f'{sim_name}.vec'], cwd=result_folder)
        p.wait()

        #os.system(scavetool_command)
    
    fileList = glob.glob(f'{os.path.join(result_folder, sim_name)}.*')
    #for filePath in fileList:
    #    os.remove(filePath)
    #os.remove(f'{os.path.join(result_folder,sim_name)}.*')
    #subprocess.Popen(['rm', f'{sim_name}.*'], cwd=result_folder)

def on_creation_carla_result_folder(result_folder, sim_name):
    # print('CARLA:', result_folder)
    ...


if __name__ == '__main__':
    # Move files to results directory

    carla_results_parent_path = './tod_analysis/archimedes_results/carla/test_carla_omnet/'
    omnet_results_parent_path = './tod_analysis/archimedes_results/omnet/'
    final_results_path = './tod_analysis/archimedes_results/tmp/'

    if not os.path.exists(final_results_path):
        os.makedirs(final_results_path)

    all_simulations_name = os.listdir(carla_results_parent_path)

    # print(all_simulations_name)
    def export_simulation(sim_name):
        carla_sim_path = os.path.join(carla_results_parent_path, sim_name)
        destination_path = os.path.join(final_results_path, sim_name)
        carla_destination_sim_path = os.path.join(destination_path, 'carla/')
        shutil.copytree(carla_sim_path, carla_destination_sim_path)
        on_creation_carla_result_folder(carla_destination_sim_path, sim_name)

        omnet_destination_sim_path = os.path.join(destination_path, 'omnet')
        os.makedirs(omnet_destination_sim_path)

        if os.path.exists(f'{omnet_results_parent_path}{sim_name}.vec') and os.path.exists(
                f'{omnet_results_parent_path}{sim_name}.sca'):
            for omnnet_file_path in glob.iglob(f'{omnet_results_parent_path}{sim_name}.*'):
                shutil.copy(omnnet_file_path, omnet_destination_sim_path)
            on_creation_omnet_result_folder(omnet_destination_sim_path, sim_name)


    #print(len(all_simulations_name), )
    with multiprocessing.Pool() as p:
        p.map(export_simulation, all_simulations_name)
        # for _ in tqdm.tqdm(, total=len(all_simulations_name)):
        #    ...
    # for simulation_name in all_simulations_name:
    #     export_simulation(simulation_name)
