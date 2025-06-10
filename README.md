# dolphin-borderless
A simple script to display and lay out both the Gamecube and GBA windows of the dolphin emulator removing borders and filling up the screen as much as possible (Windows only). 

![image](https://github.com/user-attachments/assets/039ff5ca-e1c3-4307-93ec-a91236271ba0)

# Setup
### 1. Dolphin setup
Just set one of the controllers to `GBA (Integrated)`.

<img src="https://github.com/user-attachments/assets/38318376-4a79-4c87-ac88-6ab448c39676" width="250" />

> [!NOTE]
> The script only supports one GBA port as of now, so you need to set ONLY one port as `GBA (Integrated)`.

### 2. Script setup
1. Download the script as a zip file and extract it to a directory of your choice.
  ![{9EA132BA-15CF-4FDC-92A8-7FF5D49F7834}](https://github.com/user-attachments/assets/26f71e7a-4947-4dbb-b4c0-41e2fdf7560c)

2. Download and install Python from https://www.python.org/downloads/.
3. Open a terminal window on the root directory of the script and run the following command to install all of its dependencies:
```console
pip install -r requirements.txt
```

# Running the script
1. Open the game on Dolphin emulator.
2. Open a terminal window on the root folder of the script and run the following command to start the script:
```console
python main.py
```
