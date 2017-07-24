# iMirror Project
Raspberry Pi powered Smart Mirror with Alexa Integration built in Python 3.6

## Installation and Updating
### Code
If you have [git](https://git-scn.com/book/en/v2/Getting-Started-Installing-Git) installed, clone the repository.
```
git clone https://github.com/Druanae/iMirror.git
```

_Alternatively download a zip from the Repository page._

Navigate to the folder for the repository.
```
cd iMirror
```

### Install Dependencies
#### Global
Packages:
* Python 3.6
* tkinter

Ensure you have [pip](https://pip.pypa.io/en/stable/installing/) installed.
```
sudo pip install -r requirements.txt
```

#### Arch Linux
```
sudo pacman -S python tk
```

#### Debian/Raspbian
```
sudo apt-get install python python-imaging-tk
```

### Add your API Token
Go to [darksky.net](https://darksky.net/dev/) and sign up for a developer account.

Edit **interface.py** and replace the contents of WEATHER_API_TOKEN with the secret key provided on the [account](https://darksky.net/dev/account/) page.
```python
WEATHER_API_TOKEN = '[TOKEN]' # replace with secret key provided at https://darksky.net/dev/account/
```

## Running
To run the application use the following command in the root of the repository:
```
python interface.py
```
