## Setup
```
# on Ubuntu or Debian
# (aptitude can be used unstead of apt to resolve ffmpeg package conflicts)
sudo apt update && sudo apt install ffmpeg

# on Arch Linux
sudo pacman -S ffmpeg

# on MacOS using Homebrew (https://brew.sh/)
brew install ffmpeg

# on Windows using Chocolatey (https://chocolatey.org/)
choco install ffmpeg

# on Windows using Scoop (https://scoop.sh/)
scoop install ffmpeg
```
Then setup the environment
```
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip wheel setuptools
pip install -r requirements.txt
```

## Running the app
Run run.sh as a program or launch via the command line
```
chmod a+x run.sh
bash run.sh
```

## known issues
On OSX there is aproblem with SSL certificates. Running a following command with the proper python version is a valid workaround as explained here: https://stackoverflow.com/questions/27835619/urllib-and-ssl-certificate-verify-failed-error/42334357#42334357
```
/Applications/Python\ 3.11/Install\ Certificates.command
```

## TODO
 - Add the progress bar
 - check multiple files download
 - what about launching from other folders?

