from datetime import datetime

import requests
from waste_collection_schedule import Collection  # type: ignore[attr-defined]

TITLE = "Orust"
DESCRIPTION = "Source for Orust waste collection."
URL = "https://orust.se"
##TEST_CASES ={
    "Kommunhuset": {"street_address": "Åvägen 2 -6, Henån"},
    "VOS": {"street_address": "Glimsåsvägen 3"},
        
}

API_URL = "https://va-renhallning-minasidor.orust.se/FutureWeb/SimpleWastePickup"


class Source:
    def __init__(self, street_address):
        self._street_address = street_address

    def fetch(self):
        r = requests.post(
            "{API_URL}/SearchAdress",
            {"searchText": self._street_address}
        )
        r.raise_for_status()

        address_data = r.json()
        address = None
        if address_data["Succeeded"] is True:
            if len(address_data["Buildings"]) > 0:
                address = address_data["Buildings"][0]

        if address is None:
            raise Exception("address not found")

        params = {"address": address}
        r = requests.get(
            "{API_URL}/GetWastePickupSchedule",
            params=params
        )
        r.raise_for_status()

        data = r.json()

        entries = []
        for item in data["RhServices"]:
            waste_type = item["WasteType"]
            icon = "mdi:trash-can"
            if waste_type == "Matavfall":
                icon = "mdi:leaf"
            next_pickup = item["NextWastePickup"]
            next_pickup_date = datetime.fromisoformat(next_pickup).date()
            entries.append(
                Collection(date=next_pickup_date, t=waste_type, icon=icon)
            )

        return entries
