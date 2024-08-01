from datetime import datetime

import requests
from waste_collection_schedule import Collection  # type: ignore[attr-defined]

TITLE = "Ourust"
DESCRIPTION = "Source for Orust waste collection."
URL = "https://orust.se"
TEST_CASES = {"15013600": {"facility_id": "15013600"}, "15013600": {"facility_id": 15013600}}

API_URL = "https://va-renhallning-minasidor.orust.se/FutureWeb/SimpleWastePickup"


class Source:
    def __init__(self, facility_id: int | str):
        self.facility_id: str = str(facility_id)

    def fetch(self):
        url = f"{API_URL}/GetWastePickupSchedule"
        params = {"address": f"({self.facility_id})"}
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()

        data = response.json()

        entries = []
        for item in data["RhServices"]:
            next_pickup = item["NextWastePickup"]
            if not next_pickup:
                continue

            next_pickup_date = datetime.strptime(next_pickup, "%Y-%m-%d").date()
            waste_type = item["WasteType"]
			icon = "mdi:trash-can"
            if waste_type == "Matavfall":
                icon = "mdi:leaf"
            entries.append(
                Collection(date=next_pickup_date, t=waste_type, icon=icon)
            )

        return entries
