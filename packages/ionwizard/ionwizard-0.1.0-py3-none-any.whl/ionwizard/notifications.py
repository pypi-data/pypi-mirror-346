import subprocess

from ionwizard.library_wizard import IonWorksPipWizard


def get_public_ionworks_package_names() -> list[str]:
    return ["ionwizard", "iwutil"]


def find_outdated(library_config):
    outdated_found = False
    licenses, package_names = get_packages_and_keys(library_config)
    cleaned_output = ["\nNewer versions of these ionworks packages available:\n"]
    for key in licenses:
        output = get_outdated_from_pip(key)
        for line in output:
            split_line = line.split()
            if (
                split_line
                and split_line[0] in package_names
                and line not in cleaned_output
            ):
                outdated_found = True
                cleaned_output.append("\t" + line)
    cleaned_output.append("\n")
    if outdated_found:
        print("".join(cleaned_output))


def get_outdated_from_pip(key):
    cmd = ["pip", "list", "--outdated"]
    if key:
        cmd += ["--index-url", f"{IonWorksPipWizard.get_address(key)}"]
    result = subprocess.run(
        cmd,
        capture_output=True,
    )
    output = result.stdout.decode("UTF-8").split("\n")
    return output


def get_packages_and_keys(library_config):
    lib_info = {lib["library"]: lib["key"] for lib in library_config}
    package_names = list(lib_info.keys()) + get_public_ionworks_package_names()
    licenses = list(lib_info.values()) + [None]
    return set(licenses), set(package_names)
