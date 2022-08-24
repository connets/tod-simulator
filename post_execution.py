import os, re


if __name__ == '__main__':
    carla_results_name = os.listdir('.out/carla')
    omnet_results_name = os.listdir('.out/omnet')

    omnet_general_results_name = map(lambda m: m.group(1), filter(lambda s: s is not None, map(lambda s : re.search('(.*)\.sca$', s), omnet_results_name)))
    print(list(omnet_general_results_name))