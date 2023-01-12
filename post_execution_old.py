import os, re, sys
import shutil
import itertools


def on_creation_omnet_result_folder(result_folder, sim_name):
    os.system(f'(cd {result_folder} && opp_scavetool x -F CSV-R -o omnet_results.csv {sim_name}.sca {sim_name}.vec)')


def on_creation_carla_result_folder(result_folder, sim_name):
    print('CARLA:', result_folder)


if __name__ == '__main__':
    # Move files to results directory

    carla_results_parent_path = 'tmp/carla/'
    omnet_results_parent_path = 'tmp/omnet/'
    final_results_path = 'results/'

    if not os.path.exists(final_results_path):
        os.makedirs(final_results_path)

    all_simulations_name = os.listdir(carla_results_parent_path)
    print(all_simulations_name)

    interested_omnet_extensions_results = {'vec', 'vci', 'sca'}

    for sim_name in all_simulations_name:
        carla_sim_path = carla_results_parent_path + sim_name + '/'
        destination_path = final_results_path + sim_name + '/'
        carla_destination_sim_path = destination_path + 'carla/'
        shutil.move(carla_sim_path, carla_destination_sim_path)
        on_creation_carla_result_folder(carla_destination_sim_path, sim_name)

        omnet_destination_sim_path = destination_path + 'omnet/'
        os.makedirs(omnet_destination_sim_path)
        for ext in interested_omnet_extensions_results:
            omnet_file_to_move = f'{omnet_results_parent_path}{sim_name}.{ext}'
            shutil.move(omnet_file_to_move, omnet_destination_sim_path)
        on_creation_omnet_result_folder(omnet_destination_sim_path, sim_name)
