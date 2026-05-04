
from app.database.models import Shipment
from app.database.models import ShipmentStatus
from app.database.models import ShipmentEvent
from app.services.Base_Service import Base_service



class ShipmentEventService(Base_service):
    def __init__(self,session):
        super().__init__(ShipmentEvent,session)

    async def create_shipment_event(
        self,
        shipment:Shipment,
        location:int=None,
        status:ShipmentStatus=None,
        description:str|None=None,
    )->ShipmentEvent:

        #todo: for each new location add shipment event if  shipment_status is not delivery

        if not location or not status:
            last_event=await self.get_latest_event(shipment)
            location=location if location else last_event.location
            status=status if status else last_event.status
            
        new_event=ShipmentEvent(
            location=location,
            status=status,
            description=description if description else self._generate_description(location,status),
            shipment_id=shipment.id,
        )
        return await self._add(new_event)
        
    async def get_latest_event(self,shipment:Shipment):
      timeline=shipment.timeline
      if len(timeline) == 0:
        return None
      timeline.sort(key=lambda item:item.created_at)
      return timeline[-1]

    def _generate_description(self,location:int,status:ShipmentStatus)->str:
        match status:
            case ShipmentStatus.placed:
                return f"Your order has been placed"
            case ShipmentStatus.shipped:
                return f"Your order has been shipped from location {location}"
            case ShipmentStatus.in_transit:
                return f"Your order is in transit at location {location}"
            case ShipmentStatus.delivered:
                return f"Your order has been delivered at location {location}"
            case ShipmentStatus.returned:
                return f"Your order has been returned from location {location}"
            case ShipmentStatus.cancelled:
                return f"Your order has been cancelled at location {location}"

 