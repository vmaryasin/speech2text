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
bash install.sh
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
 - package everything properly
 - Add the progress bar to streamlit
 - what about launching from other folders?
 - can I do better than hardcoding my token?

