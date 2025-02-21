import os, sys, shutil, subprocess

BASE_DIR = "C:/HdM-DT"

# looks for a valid git.exe

def git_path():
    path = "C:/Program Files/Git/bin/git.exe"  # local installed git location
    if not os.path.exists(path):
        path = "//hersrv01/Bibliothek/03_DigitalTechnologiesGroup/20_SOFTWARE/git/bin/git.exe"  # fallback portable git location
    if not os.path.exists(path):
        print("CRITICAL: no git.exe found.")
        sys.exit(1)
    return path

# helper function to split command string into arguments, preserving quoted substrings

def split_command(command):
    import re
    tokens = re.findall(r'"([^"]+)"|(\S+)', command)
    return [t[0] if t[0] else t[1] for t in tokens]

# execute a git command via subprocess using a list of arguments

def git_command(command, cwd=""):
    if not cwd:
        cwd = None
    args = [git_path()] + split_command(command)
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startupinfo.wShowWindow = 0
    try:
        output = subprocess.check_output(args, stderr=subprocess.STDOUT, cwd=cwd, startupinfo=startupinfo)
        return output
    except subprocess.CalledProcessError as e:
        print("Command failed: {}".format(e.output))
        return False

# determines a valid installation directory for the repository

def ensure_installdir(repo_url, install_dir="", create_subfolder=True):
    if install_dir and install_dir != BASE_DIR:
        install_dir = os.path.join(BASE_DIR, install_dir)
    else:
        install_dir = BASE_DIR
    if not repo_url.endswith(".git"):
        print("CRITICAL: The url '{}' is not a valid repo url".format(repo_url))
        return False
    if create_subfolder:
        repo_name = repo_url[:-4].split("/")[-1]
        install_dir = os.path.join(install_dir, repo_name)
    return install_dir

# clones the repository; if it exists, removes the directory to force reinstallation

def clone_repository(repo_url, install_dir):
    if os.path.exists(install_dir):
        shutil.rmtree(install_dir)
    clone_cmd = "clone \"{}\" \"{}\"".format(repo_url, install_dir)
    print("Cloning repository: {}".format(clone_cmd))
    result = git_command(clone_cmd)
    if result is False:
        print("Failed to clone repository")
    else:
        print("Repository cloned to {}".format(install_dir))
    return result

# pulls the latest changes from the repository

def pull_repository(install_dir):
    print("Pulling latest changes in {}".format(install_dir))
    result = git_command("pull", install_dir)
    if result is False:
        print("Failed to pull changes")
    else:
        print("Repository updated")
    return result

# installs or updates the repository: clones if not present, pulls if it is
# If an install.py file exists in the repository, it is executed.

def install_or_update(repo_url, folder_name="", create_subfolder=False):
    install_dir = ensure_installdir(repo_url, folder_name, create_subfolder)
    if not install_dir:
        return False
    if os.path.exists(install_dir) and os.path.isdir(os.path.join(install_dir, ".git")):
        pull_repository(install_dir)
    else:
        clone_repository(repo_url, install_dir)
    
    # Check for and run install.py if it exists
    install_py = os.path.join(install_dir, "install.py")
    if os.path.isfile(install_py):
        print("Running {}".format(install_py))
        try:
            output = subprocess.check_output([sys.executable, install_py], stderr=subprocess.STDOUT, creationflags=subprocess.CREATE_NO_WINDOW)
            print("install.py output: {}".format(output))
        except subprocess.CalledProcessError as e:
            print("Failed to run install.py: {}".format(e.output))
    return True

if __name__ == "__main__":
    # for installer testing
    test_dir = os.path.join(BASE_DIR, "test")
    install_or_update("https://github.com/herzogdemeuron/demo-repository.git", folder_name="test") 