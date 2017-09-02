# iMirror Project
Raspberry Pi Powered Smart Mirror Built in Python 3.6

## Installation and Updating
### Code
If you have [git](https://git-scn.com/book/en/v2/Getting-Started-Installing-Git) installed, clone the repository.
```
git clone https://github.com/Druanae/iMirror.git
```

_Alternatively download a zip from the Repository page._

Navigate to the folder for the repository.
```bash
cd iMirror
```

### Install Dependencies
#### Global
Packages:
* Python 3.6
* tkinter

Ensure you have [pip](https://pip.pypa.io/en/stable/installing/) installed.
```bash
sudo pip install -r requirements.txt
```

#### Font
Install the Lato fonts in the font folder.
```bash
mkdir ~/.fonts
cp fonts/* ~/.fonts
fc-cache -vf .fonts
```

#### Arch Linux
```bash
sudo pacman -S python tk
```

#### Debian/Raspbian
```bash
sudo apt-get install python python-imaging-tk
```

### Add your API Token
Go to [darksky.net](https://darksky.net/dev/) and sign up for a developer account.

Edit **interface.py** and replace the contents of WEATHER_API_TOKEN with the secret key provided on [Darksky's account page](https://darksky.net/dev/account/).
```python
WEATHER_API_TOKEN = '[TOKEN]' # replace with secret key provided at https://darksky.net/dev/account/
```

## Running
To run the application use the following command in the root of the repository:
```bash
python interface.py
```
