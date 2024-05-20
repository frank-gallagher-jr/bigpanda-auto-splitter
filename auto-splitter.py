import sys
import requests

# Credentials Required 

api_key = ""  #  Add User API Key which looks like "BPU1234..."

###############################################################################################################################
#    ___            __                  _____             __    _    __    __               
#   /   |  __  __  / /_  ____          / ___/    ____    / /   (_)  / /_  / /_  ___    _____
#  / /| | / / / / / __/ / __ \ ______  \__ \    / __ \  / /   / /  / __/ / __/ / _ \  / ___/
# / ___ |/ /_/ / / /_  / /_/ //_____/ ___/ /   / /_/ / / /   / /  / /_  / /_  /  __/ / /    
#/_/  |_|\__,_/  \__/  \____/        /____/   / .___/ /_/   /_/   \__/  \__/  \___/ /_/     
#                                            /_/      
###############################################################################################################################
#  Frank Gallagher | BigPanda Solution Architect | May 2024 - https://github.com/frank-gallagher-jr                                      
###############################################################################################################################
#
#  PURPOSE:  This script will take a highly correlated event in BigPanda and split ALL 
#            correlated alerts into individual BigPanda incidents.  
#
#  USE CASE:  You made a mistake or you were not strict enough with correlation and you 
#             accidentally correlated alerts which shouldn't be correlated together 
#             (generally due to poor source data quality and generic use of tag values)
#
#             For example:  Let's say you have a correlation pattern of "Service" which 
#                 looks for opportunities to group alerts together over 2 hours.
#                 If alerts come in from an observability host with a generic Service
#                 such as "Monitoring" due to a generic payload issue, you may find out
#                 that the correlation pattern needs to be updated far too late to
#                 prevent this unwanted behavior. 
#
#               Auto-Splitter takes your environment ID (found in the URL of BigPanda)
#               and the incident ID (found in the URL of BigPanda) and automatically
#               splits all of the alerts out into their own new BigPanda Incidents.
#
#               This saves manual operations in the BigPanda UI which would be tedious.
#
#  USAGE:  python3 auto-splitter.py <Insert Environment ID>  <Insert Incident ID to be fully split>
###############################################################################################################################
#  USE WITH CAUTION AND USE WISELY!  Note:  The Split function is asynchronous.  
#  Read more about the API here:  https://docs.bigpanda.io/reference/split-incident
###############################################################################################################################

def get_alert_ids(environment_id, incident_id):
    url = f"https://api.bigpanda.io/resources/v2.0/environments/{environment_id}/incidents/{incident_id}"
    headers = {
        'Authorization': f'Bearer {api_key}'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return [alert['alert_id'] for alert in data['alerts']]
    else:
        print(f"Error retrieving incident data: {response.status_code} - {response.text}")
        return None

def split_incident(environment_id, incident_id, alert_id):
    url = f"https://api.bigpanda.io/resources/v2.0/environments/{environment_id}/incidents/{incident_id}/split"
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    data = {
        "comment": "Split by Auto-Splitter Script",
        "alerts": [alert_id]
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code in [200, 202]:
        print(f"Alert {alert_id} split successfully and is being processed.")
    else:
        print(f"Error splitting alert {alert_id}: {response.status_code} - {response.text}")

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 script.py <environment_id> <incident_id>")
        sys.exit(1)
    
    environment_id, incident_id = sys.argv[1], sys.argv[2]
    alert_ids = get_alert_ids(environment_id, incident_id)
    
    if alert_ids:
        for alert_id in alert_ids[:-1]:  # Exclude the last alert
            split_incident(environment_id, incident_id, alert_id)

if __name__ == "__main__":
    main()
