import json


shipments = {}

with open("shipments.json") as open_file:
    data = json.load(open_file)
    for item in data:
        shipment_id = item["id"]
        shipments[shipment_id] = {
            "id": item["id"],
            "weight": item["weight"],
            "content": item["content"],
            "destination": item.get("destination"),
            "status": item["status"]
        }

def save_shipments():
    with open("shipments.json","w") as open_file:
        json.dump(
            list(shipments.values()),
            open_file
        )