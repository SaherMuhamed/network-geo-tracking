import requests
import dpkt
import socket
import pygeoip
import sys

geoip_obj = pygeoip.GeoIP("geo-city.dat")


def get_public_ip():
    """this function to get public IP using an external service"""
    try:
        response = requests.get("https://api.ipify.org?format=json")
        if response.status_code == 200:
            return response.json()["ip"]
        else:
            raise Exception("Failed to retrieve public IP")
    except Exception as e:
        print("Error getting public IP:", str(e))
        return None


def generate_kml(dst_ip, src_ip):
    """This function translates IP addresses to geolocation addresses"""
    dst = geoip_obj.record_by_name(dst_ip)
    src = geoip_obj.record_by_name(src_ip)

    if dst is None or src is None:
        # print("Error: Could not find geolocation information for one or both IPs.")
        return ''

    try:
        dst_latitude = dst.get("latitude", 0.0)
        dst_longitude = dst.get("longitude", 0.0)
        src_latitude = src.get("latitude", 0.0)
        src_longitude = src.get("longitude", 0.0)

        return ('<Placemark>\n<name>%s</name><extrude>1</extrude>\n<tessellate>1</tessellate>\n'
                '<styleUrl>#transBluePoly</styleUrl>\n<LineString>\n'
                '<coordinates>%f,%f\n%f,%f</coordinates>\n</LineString>\n</Placemark>\n') % (
               dst_ip, dst_longitude, dst_latitude, src_longitude, src_latitude)
    except Exception as e:
        pass
        # print("Error generating KML for IPs:", dst_ip, src_ip)
        # print(str(e))
        return ''


def plot_ip(pcap, public_ip):
    kml_pts = ''
    for (ts, buf) in pcap:
        try:
            ether = dpkt.ethernet.Ethernet(buf)
            ip_addr = ether.data
            # src = socket.inet_ntoa(ip_addr.src)  # since I use get_public_ip() function I don't need it
            dst = socket.inet_ntoa(ip_addr.dst)
            kml = generate_kml(dst, public_ip)  # Pass public IP as source IP
            kml_pts += kml
        except Exception as e:
            pass
            # print("Error processing packet:", str(e))
    return kml_pts


def main():
    if len(sys.argv) != 2:
        print("[+] Usage: %s <.pcap>" % sys.argv[0])
        print("[+] Example: %s wireshark.pcap" % sys.argv[0] + "\n")
        sys.exit(-1)
    print("[*] start generating kml file for given file...")
    file = sys.argv[1]
    public_ip = get_public_ip()
    if public_ip:
        with open(file=file, mode="rb") as pcap_file:
            pcap = dpkt.pcap.Reader(fileobj=pcap_file)
            kml_header = '<?xml version="1.0" encoding="UTF-8"?>\n<kml xmlns="http://www.opengis.net/kml/2.2">\n<Document>\n<Style id="transBluePoly"><LineStyle><width>1.7</width><color>445D48</color></LineStyle></Style>'
            kml_footer = '</Document>\n</kml>\n'
            kml_document = kml_header + plot_ip(pcap, public_ip) + kml_footer

            with open(file="traffic.kml", mode="w") as kml_file:
                kml_file.write(kml_document)
    print("[+] generated " + kml_file.name + " file successfully")


if __name__ == "__main__":
    main()
