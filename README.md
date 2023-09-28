# Network Tracking Analysis
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

This Python project, "Network Tracking Analysis," is designed to analyze network traffic data captured in a `.pcap` file and generate a **KML (Keyhole Markup Language)** file that can be used to visualize the geolocation information of the network traffic. It utilizes various libraries like requests, dpkt, socket, and pygeoip to accomplish this task.

## Features
1. Retrieve your public IP address using an external service.

2. Translate IP addresses to geolocation coordinates.

3. Generate a KML file with geolocation information for network traffic.

4. Visualize network traffic geolocation data in tools like *Google Earth*.

## Prerequisites
Before you get started, ensure that you have the following dependencies installed:

- `Python 3.x`
- `requests` library
- `dpkt` library
- `pygeoip` library
- A GeoIP database file named `"geo-city.dat"`

    ```commandline
    pip install requests dpkt pygeoip
    ```

## Screenshots
![](screenshots\Screenshot_2023-09-28_233923.png)

![](screenshots\Screenshot_2023-09-28_234009.png)


## Usage
- Clone this repository or download the project files to your local machine.

- Make sure you have the `"geo-city.dat"` GeoIP database file in the same directory as the project.

- Open a terminal or command prompt.

- Run the script by providing the path to the .pcap file as a command-line argument:

    ```commandline
    python main.py wireshark.pcap
    ```

- Replace `wireshark.pcap` with the path to your own `.pcap` file.

- The script will process the network traffic data, generate a KML file named `"traffic.kml,"` and save it in the same directory.

- You can open the "traffic.kml" file in Google Earth or any KML-compatible application to visualize the geolocation information of the network traffic.
