from falconpy import Hosts
import csv
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("CLIENTID")
API_SECRET = os.getenv("CLIENTSECRET")

def device_list(off: int, limit: int, sort: str):
    """Return a list of all devices for the CID, paginating when necessary."""
    result = falcon.query_devices_by_filter(limit=limit, offset=off, sort=sort)
    new_offset = 0
    total = 0
    returned_device_list = []
    if result["status_code"] == 200:
        new_offset = result["body"]["meta"]["pagination"]["offset"]
        total = result["body"]["meta"]["pagination"]["total"]
        returned_device_list = result["body"]["resources"]

    return new_offset, total, returned_device_list

def device_detail(aids: list):
    """Return the device_id and agent_version for a list of AIDs provided."""
    result = falcon.get_device_details(ids=aids)
    device_details = []
    if result["status_code"] == 200:
        # return just the aid and agent version
        for device in result["body"]["resources"]:
            res = {}
            res["hostname"] = device.get("hostname", None)
            res["last_seen"] = device.get("last_seen", None)
            res["agent_version"] = device.get("agent_version", None)
            res["platform_name"] = device.get("platform_name", None)
            res["os_version"] = device.get("os_version", None)
            res["ou"] = device.get("ou", None)
            res["tags"] = device.get("tags", None)
            device_details.append(res)
    return device_details

falcon = Hosts(client_id=API_KEY,
               client_secret=API_SECRET,
               )

OFFSET = 0      # Start at the beginning
DISPLAYED = 0   # Running count
TOTAL = 1       # Assume there is at least one
LIMIT = 500     # Quick limit to prove pagination
SORT = "agent_version.asc"

workstations_data = []
windows_servers_data = []
linux_servers_data = []
#sensor version you wish to compare to
while OFFSET < TOTAL:
    OFFSET, TOTAL, devices = device_list(OFFSET, LIMIT, SORT)
    details = device_detail(devices)
    for detail in details:
        agent_version = detail['agent_version']
        hostname = detail['hostname']
        os = detail['platform_name'].lower()
        os_version = detail['os_version']
        ou = detail['ou']
        tag = detail['tags']
        tag_string = ", ".join(tag)
        if ou != None:
            ou_lower = [x.lower() for x in ou]
        agent_versions = detail
        #data for workstations
        if  ou_lower != None and ("workstations" in ou_lower and "workspaces" not in ou_lower) and "FalconGroupingTags/old_sensors" in tag_string:
            DISPLAYED += 1
            workstations_data.append([hostname, agent_version, os])
            #print(f"{DISPLAYED}: Hostname: {hostname} Agent Version: {agent_version} {tag_string}")
        #data for windows servers
        if  ou_lower != None and ("servers" in ou_lower) and os == "windows" and "FalconGroupingTags/old_sensors" in tag_string:
            DISPLAYED += 1
            windows_servers_data.append([hostname, agent_version, os])
            #print(f"{DISPLAYED}: Hostname: {hostname} Agent Version: {agent_version}")
        # data for linux servers
        if  ou_lower != None and ("servers" in ou_lower) and os == "linux" and "FalconGroupingTags/old_sensors" in tag_string:
            DISPLAYED += 1
            linux_servers_data.append([hostname, agent_version, os])
            #print(f"{DISPLAYED}: Hostname: {hostname} Agent Version: {agent_version}")

with open('workstations_results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Hostname', 'Version', 'os'])
    writer.writerows(workstations_data)
with open('windows_servers_results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Hostname', 'Version', 'os'])
    writer.writerows(windows_servers_data)
with open('linux_servers_results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Hostname', 'Version', 'os'])
    writer.writerows(linux_servers_data)

if not DISPLAYED:
    print("No results returned.")
