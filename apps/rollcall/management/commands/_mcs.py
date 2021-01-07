import requests
import time


class Device:
    BASE_URL = "https://api.mediatek.com/mcs/v2"

    def __init__(self, device_id, device_key):
        self.device_url = f"{self.BASE_URL}/devices/{device_id}"
        self.device_key = device_key

    def retrieve_values(self, channel_id):
        response = requests.get(
            url=f"{self.device_url}/datachannels/{channel_id}/datapoints",
            headers={"deviceKey": self.device_key},
        )
        response.raise_for_status()
        return response.json()["dataChannels"][0]["dataPoints"][0]["values"]

    def upload_values(self, channel_id, values):
        response = requests.post(
            url=f"{self.device_url}/datapoints",
            headers={"deviceKey": self.device_key},
            json={
                "datapoints": [
                    {
                        "dataChnId": channel_id,
                        "timestamp": int(time.time()),
                        "values": values,
                    }
                ]
            },
        )
        response.raise_for_status()
