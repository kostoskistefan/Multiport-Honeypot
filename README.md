# Multi-Port Honeypot [![version](https://img.shields.io/badge/version-1.0-red.svg)](https://semver.org)

Very simple Python honeypot that can run on multiple ports on a single machine. It can detect if someone is scanning your network or tampering with the specified honeypot ports. 

## Requirements
* Any version of Python3

## Installation
Clone the repository using `git clone https://github.com/kostoskistefan/multiport-honeypot.git`

Change to the cloned directory `cd multiport-honeypot`

Run the script `python3 honeypot.py [OPTIONS]`

## Options

* `-p / --ports` - A list of comma separated ports

* `-a / --host` - IP address of the network interface on your local machine

* `-o / --output` - Path to the directory where the log will be saved

If the `output` flag is not specified, it will use the same folder in which the script is located.

## Output
The output log contains the following information:
* Timestamp of each connection
* IP address of the attacker
* Port from which the attacker made the connection

## Usage examples

`$ python3 honeypot.py -p 21,23,123 -a 192.168.0.105` - It will open the ports 21, 23 and 123 and wait for an incoming connection. 

`$ python3 honeypot.py -p 21,23,123 -a 192.168.0.105 -o /home/user/logs` - Same as the previous one, except it will save the log file in `/home/user/logs/honey.log`
