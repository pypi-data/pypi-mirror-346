import os
import yaml
import uuid
import pathlib
import machineid
from platformdirs import user_config_dir


class WriteConfig:
    @staticmethod
    def save_config(config, path: str | pathlib.Path):
        if "user_id" not in config:
            config["user_id"] = str(uuid.uuid4())
        config["machine_id"] = machineid.id()
        with open(path, "w") as f:
            yaml.dump({"ionworks": config}, f)

    @staticmethod
    def get_config_path():
        config_dir = pathlib.Path(user_config_dir("ionworks"))
        config_dir.mkdir(parents=True, exist_ok=True)
        return config_dir / "config.yml"

    @staticmethod
    def create_config_for(product: str, use_pip_conf: bool = True):
        if use_pip_conf:
            license_key = WriteConfig.read_pip_conf()
        else:
            raise NotImplementedError(
                "Configs can only be created from pip.conf files."
            )
        return {
            "libraries": {"library": product, "key": license_key, "install": "false"}
        }

    @staticmethod
    def write_config_to_disk(library_name: str):
        product_config = WriteConfig.create_config_for(library_name)
        WriteConfig.save_config(product_config, WriteConfig.get_config_path())

    @staticmethod
    def read_pip_conf():
        pip_conf = WriteConfig.get_conf_file()
        return WriteConfig.get_key_from(pip_conf)

    @staticmethod
    def get_key_from(pip_conf):
        start_string = "license:"
        end_string = "@api.keygen.sh"
        with open(pip_conf) as p:
            pip_url = None
            for line in p.readlines():
                if end_string in line:
                    pip_url = line
            if pip_url is None:
                raise ValueError("No pip index URL was found.")
        start = pip_url.find(start_string) + len(start_string)
        end = pip_url.find(end_string)
        key = pip_url[start:end]
        return key

    @staticmethod
    def get_conf_file():
        pip_conf = None
        for opt in ["pip.conf", "pip.ini"]:
            if os.path.exists(opt):
                pip_conf = opt
                break
        if pip_conf is None:
            raise FileNotFoundError("No pip config file was found.")
        return pip_conf
