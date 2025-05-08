import argparse


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", type=str, required=False)
    config_args, pip_args = parser.parse_known_args()
    config_name = config_args.c
    return config_name, pip_args
