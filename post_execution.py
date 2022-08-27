import os, re, sys
import shutil
import itertools

if __name__ == '__main__':

    # Move files to results directory
    carla_results_parent_path = '.out/carla/'
    omnet_results_parent_path = '.out/omnet/'
    final_results_path = 'results/'
    if not os.path.exists(final_results_path):
        os.makedirs(final_results_path)

    #carla_results_path = map(lambda r: carla_results_parent_path + r, os.listdir(carla_results_parent_path))
    omnet_results_path = map(lambda r: omnet_results_parent_path + r, os.listdir(omnet_results_parent_path))

    omnet_general_results_path = map(lambda m: (m.group(1),next(itertools.islice(open(m.group(), 'r'), 1, None))[4:-1]), 
        filter(lambda s: s is not None, 
            map(lambda s : re.search('(.*)\.sca$', s), omnet_results_path)))

    #print(list(carla_results_pat))
    interested_omnet_extensions_results = {'.vec', '.vci', '.sca'}
    for omnet_result_name, run_id in omnet_general_results_path:
        carla_result_path = carla_results_parent_path + run_id + '/'
        if os.path.exists(carla_result_path):
            shutil.move(carla_result_path, final_results_path)
            destination_path = final_results_path + run_id
            for ext in interested_omnet_extensions_results:
                omnet_file_to_move = omnet_result_name + ext
                shutil.move(omnet_file_to_move, destination_path)


    # Extract omnet file