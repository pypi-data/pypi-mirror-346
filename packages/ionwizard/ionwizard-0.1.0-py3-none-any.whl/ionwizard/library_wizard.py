import yaml
import subprocess
from ionwizard.write_config import WriteConfig
from ionwizard.env_variables import KEYGEN_ACCOUNT_ID
from ionwizard.input_args import get_arguments


class IonWorksPipWizard:
    @staticmethod
    def get_address(key: str):
        head = "https://license:"
        middle = "@api.keygen.sh/v1/accounts/"
        account = KEYGEN_ACCOUNT_ID
        tail = "/engines/pypi/simple"
        return head + key + middle + account + tail

    @staticmethod
    def install_library(lib_name, web_address):
        err = subprocess.call(["pip", "install", lib_name, "--index-url", web_address])
        if err != 0:
            print(f"\nInstallation failed for {lib_name}.\n")

    @staticmethod
    def install_from(config):
        for library in config["libraries"]:
            addr = IonWorksPipWizard.get_address(library["key"])
            if library["install"]:
                IonWorksPipWizard.install_library(library["library"], addr)

    @staticmethod
    def process_config(file_name):
        with open(file_name) as f:
            config = yaml.safe_load(f)
        if "libraries" not in config:
            raise ValueError("Invalid configuration file.")
        return config

    @staticmethod
    def save_config(config):
        config_path = WriteConfig.get_config_path()
        WriteConfig.save_config(config, config_path)


def run():
    try:
        config_file, _ = get_arguments()
        processed_config = IonWorksPipWizard.process_config(config_file)
        IonWorksPipWizard.install_from(processed_config)
        IonWorksPipWizard.save_config(processed_config)
    except (IndexError, FileNotFoundError, TypeError):
        print("\nUsage:\n\tionwizard-library -c <config file>\n")


if __name__ == "__main__":
    run()
