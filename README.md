# openprompter-beta
Beta version of the OpenPrompter Software (OPR/OPS) suite

## Introduction

This project provided the teleprompting software for Whitney HS Live,
2022-23. The deployment there was with 3 prompters and 1 CNC.

OPS-beta is an open-source teleprompting software, primarily designed
for *nix (tested on Linux and macOS) devices. It's a simpler piece of
software, as it was particularly tailored for the Whitney HS Live use 
cases.

## Installation

Download the repository (requires Git):

```sh
git clone https://github.com/amyipdev/openprompter-beta
```

### Command-and-control

Copy and edit the server control file:
```sh
cd cnc
cp cncsets.json.example cncsets.json
$EDITOR cncsets.json
```

Create a virtual environment and install Requests:
```sh
cd ..
python3 -m venv venv
cd cnc
source ../venv/bin/activate
pip3 install requests
```
(For future loads, just run the `source` command)

Run the client:
```sh
python3 cnc.py
```

### Teleprompters

Run the setup script:
```sh
cd server
./setup.sh
```

Modify the config files:
```sh
$EDITOR discovsets.json
$EDITOR appsets.json
$EDITOR pygsets.json
```

## Configuration

### `cncsets.json`

* `network_broadcast`: broadcast address for the network (such as `10.255.255.255`)
* `challenge`: challenge phrase for `discov` (should match `discovsets.json:trigger`)
* `resp`: success response (should match `discovsets.json:response`)
* `timeout`: timeout for `discov`
* `discovport`: port to send `discov` broadcast on (standard: 61910, should match `discovsets.json:port`)
* `appport`: port to send commands on (standard: 61911, should match `appsets.json:port`)

### `appsets.json`

* `host`: bind address for server (recommended either `0.0.0.0` or `[::]`)
* `port`: port for commands (standard: 61911, should match `cncsets.json:appport`)
* `pid`: default name for server
* `prev_lines`: number of lines to send as a preview

### `discovsets.json`

* `host`: bind address (recommended: `""`)
* `port`: port for `discov` (standard: 61910, should match `cncsets.json:discovport`)
* `trigger`: challenge phrase (should match `cncsets.json:trigger`)
* `response`: success response (should match `cncsets.json:resp`)

### `pygsets.json`

* `mode`: current viewing mode (AUTO)
* `scriptfile`: current script viewing file (AUTO)
* `lpos`: line position (AUTO)
* `fontfile`: file containing screen font
* `fontsize`: font size
* `dim_x`: window width
* `dimA_x`: camera width
* `dim_y`: window height
* `dimA_y`: camera height
* `inset`: top padding for text
* `fps`: screen fps (set lower on low-power devices)
* `fullscreen`: whether to use fullscreen

## Operation

In the OPS model, there are many teleprompters on a network, all served by a single command and control node.
At any given time, only one prompter can be active; you can also have no prompters be active. When a prompter
is inactive, it shows the camera view being fed into that prompter; otherwise, it shows whatever script is
currently loaded.

First, on each teleprompter, launch the server:
```sh
./launch.sh
```

You should get a prompt along the lines of:
```
[cnc@ops None]$
```

This is the OpenPrompter prompt. All the following commands should be run there.
To leave the prompt and close the CNC, run `q` or `quit.`

By default, OPS assumes you have a teleprompter running on your CNC server. This is a rare use case;
if it applies, you don't need to do anything. Otherwise, run `drop lo`. In general, to remove a prompter,
use `drop <name>` (alternatively, `delink <name>`). You can list your prompters using `p`, `conns`, or `showdev`.
To test that a connection works, use `ping <name>`.

To find teleprompters on your network, run `discov`. It will pick up the first, and only the first,
teleprompter to respond. If you don't want to add that teleprompter, press `Ctrl-C`. Otherwise, give 
it a name (leaving it blank uses the default name) and press enter; this name will be used for
selecting the prompter. You can run discov as many times as you need to add all your prompters; this
will need to be done each time the CNC is restarted. If you're having issues getting your prompters
online, we recommend selectively connecting them to the network, one at a time; as long as the IP
addresses don't reset, the connection will be maintained.

Before you activate a prompter, you need to load a script on it. You can transmit a script
from your CNC's local directory using `csc <servername> <filename>`. Once a script you want
to load exists, you can load it using `lsc <servername> <filename>`. 

Activating a prompter will deactivate the current one. To deactivate all prompters, run `flush`.
To deactivate the current prompter, run `s None`, `sel None`, or `select None`. To activate
a prompter run `s <name>`, `sel <name>`, or `select <name>`. This will jump the script to the
first line, even if loaded previously; to perform the same jump at any time, run `z`.

You will consistently get a preview of the lines being shown on the screen; it may not be fully
accurate depending on the size of the display. This is configurable in `appsets.json:prev_lines`.

To advance the current prompter's line by 1, run `1`; to rewind it by 1, run `2`. These are considered
fast commands, and recommended for usage when manually moving a prompter. To jump by a certain amount, 
use `d <num>` to advance, and `u <num>` to rewind by `<num>` lines.

If you know the rough pace of your speaker, you can use `mt <lines> <interval>`. This will
automatically advance 1 line every `<interval>` seconds for `<lines>` lines. This can always be
interrupted with `Ctrl-C`.

## Known Issues

On lower-power hardware, crashes can occur if the files are not updated before the 
modification date changes. If this happens regularly to you, contact me; I can provide
you with a patch for your particular hardware/troubleshooting support.

You must have a camera connected, and working (thus not taken up by another application)
to launch OPS. If you lose camera connection, OPS will crash.

If the teleprompter's IP address changes, you will need to drop that prompter and re-add it.

Fullscreen is broken on many devices, and has even been shown to require a device
restart if activated. It is known to work properly on Raspbian and Ubuntu, however.

## License and Copyright

Copyright (C) Amy Parker, 2022-2023. All rights reserved.

This project is free software; it is distributed to you under the terms of the GNU General
Public License, version 2, or (at your option) any later version. See the LICENSE file for
details, or go to https://www.gnu.org/licenses/ for a copy of the license.
