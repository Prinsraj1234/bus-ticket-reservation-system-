import json
from datetime import datetime, timedelta
from pathlib import Path
import uuid

DATA_FILE = Path("data.json")
ROUTES = {
    "R1": {"name": "Bhopal to Indore", "base_fare": 500, "departure": "2026-10-05 09:00"},
    "R2": {"name": "Bhopal to Jabalpur", "base_fare": 450, "departure": "2026-10-05 14:00"},
    "R3": {"name": "Bhopal to Gwalior", "base_fare": 550, "departure": "2026-10-06 08:30"},
}

SEAT_COUNT = 20
CANCELLATION_DEDUCTION = {
    "more_than_24h": 0.10,
    "6_to_24h": 0.25,
    "less_than_6h": 0.50,
}

def load_data():
    if not DATA_FILE.exists():
        return {"bookings": [], "cancelled_routes": []}
    with DATA_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)

def save_data(data):
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)

def get_route(route_id):
    return ROUTES.get(route_id.upper())

def show_routes(data):
    print("\nAvailable routes")
    print("-" * 70)
    for route_id, route in ROUTES.items():
        status = "CANCELLED" if route_id in data["cancelled_routes"] else "Running"
        print(f"{route_id}: {route['name']} | Departure: {route['departure']} | "
              f"Base fare: Rs.{route['base_fare']} | {status}")

def available_seats(data, route_id):
    booked = {
        booking["seat"]
        for booking in data["bookings"]
        if booking["route_id"] == route_id and booking["status"] == "CONFIRMED"
    }
    return [seat for seat in range(1, SEAT_COUNT + 1) if seat not in booked]

def show_seats(data, route_id):
    seats = available_seats(data, route_id)
    print("\nSeat status:")
    for seat in range(1, SEAT_COUNT + 1):
        mark = "Available" if seat in seats else "Occupied"
        print(f"{seat:2}: {mark}", end=" ")
        if seat % 4 == 0:
            print()
    print()

def calculate_fare(base_fare, category):
    category = category.lower()
    discounts = {"adult": 0.0, "child": 0.30, "senior": 0.20}
    if category not in discounts:
        raise ValueError("Passenger category must be adult, child, or senior.")
    return round(base_fare * (1 - discounts[category]), 2)

def payment():
    choice = input("Payment method (1=UPI, 2=Card): ").strip()
    if choice not in {"1", "2"}:
        print("Invalid payment method.")
        return False
    result = input("Enter P for successful payment or F for failure: ").strip().upper()
    return result == "P"

def book_ticket(data):
    show_routes(data)
    route_id = input("\nEnter route ID: ").strip().upper()
    route = get_route(route_id)
    if not route:
        print("Invalid route.")
        return
    if route_id in data["cancelled_routes"]:
        print("This trip has been cancelled. Booking is not allowed.")
        return
    show_seats(data, route_id)
    try:
        seat = int(input("Choose seat number: "))
    except ValueError:
        print("Seat number must be numeric.")
        return
    if seat not in available_seats(data, route_id):
        print("That seat is already occupied or invalid. Double booking prevented.")
        return
    name = input("Passenger name: ").strip()
    category = input("Category (adult/child/senior): ").strip().lower()
    try:
        fare = calculate_fare(route["base_fare"], category)
    except ValueError as error:
        print(error)
        return
    print(f"Fare to pay: Rs.{fare:.2f}")
    if not payment():
        print("Payment failed. No ticket was created and the seat remains available.")
        return
    booking_id = "BUS-" + uuid.uuid4().hex[:8].upper()
    booking = {
        "booking_id": booking_id,
        "name": name,
        "route_id": route_id,
        "seat": seat,
        "category": category,
        "fare": fare,
        "booked_at": datetime.now().isoformat(timespec="minutes"),
        "status": "CONFIRMED",
    }
    data["bookings"].append(booking)
    save_data(data)
    print("\nTicket issued successfully.")
    print_ticket(booking)

def print_ticket(booking):
    route = ROUTES[booking["route_id"]]
    print("-" * 50)
    print(f"Ticket ID : {booking['booking_id']}")
    print(f"Passenger : {booking['name']}")
    print(f"Route : {route['name']}")
    print(f"Departure : {route['departure']}")
    print(f"Seat : {booking['seat']}")
    print(f"Category : {booking['category'].title()}")
    print(f"Fare : Rs.{booking['fare']:.2f}")
    print(f"Status : {booking['status']}")
    print("-" * 50)

def find_booking(data, booking_id):
    for booking in data["bookings"]:
        if booking["booking_id"].upper() == booking_id.upper():
            return booking
    return None

def cancellation_refund(booking):
    departure = datetime.strptime(
        ROUTES[booking["route_id"]]["departure"], "%Y-%m-%d %H:%M"
    )
    hours_left = (departure - datetime.now()).total_seconds() / 3600
    if hours_left <= 0:
        return 0, "Departure time has passed. No refund."
    if hours_left > 24:
        rate = CANCELLATION_DEDUCTION["more_than_24h"]
        return round(booking["fare"] * (1 - rate), 2), "10% cancellation deduction."
    if hours_left >= 6:
        rate = CANCELLATION_DEDUCTION["6_to_24h"]
        return round(booking["fare"] * (1 - rate), 2), "25% cancellation deduction."
    rate = CANCELLATION_DEDUCTION["less_than_6h"]
    return round(booking["fare"] * (1 - rate), 2), "50% cancellation deduction."

def cancel_ticket(data):
    booking_id = input("Enter ticket ID: ").strip()
    booking = find_booking(data, booking_id)
    if not booking:
        print("Ticket not found.")
        return
    if booking["status"] != "CONFIRMED":
        print("This ticket is already cancelled.")
        return
    refund, message = cancellation_refund(booking)
    if refund == 0:
        print(message)
        return
    booking["status"] = "CANCELLED"
    booking["refund"] = refund
    booking["cancelled_at"] = datetime.now().isoformat(timespec="minutes")
    save_data(data)
    print(f"Ticket cancelled. {message}")
    print(f"Refund amount: Rs.{refund:.2f}")

def cancel_route(data):
    show_routes(data)
    route_id = input("Enter route ID to cancel: ").strip().upper()
    if route_id not in ROUTES:
        print("Invalid route.")
        return
    if route_id in data["cancelled_routes"]:
        print("Route is already cancelled.")
        return
    data["cancelled_routes"].append(route_id)
    for booking in data["bookings"]:
        if booking["route_id"] == route_id and booking["status"] == "CONFIRMED":
            booking["status"] = "CANCELLED"
            booking["refund"] = booking["fare"]
            booking["cancelled_at"] = datetime.now().isoformat(timespec="minutes")
    save_data(data)
    print("Trip cancelled. Confirmed bookings on this trip have been marked cancelled with full refund.")

def view_tickets(data):
    confirmed = [b for b in data["bookings"] if b["status"] == "CONFIRMED"]
    if not confirmed:
        print("No confirmed tickets.")
        return
    for booking in confirmed:
        print_ticket(booking)

def main():
    data = load_data()
    while True:
        print("\n=== BUS TICKET RESERVATION SYSTEM ===")
        print("1. View routes and seats")
        print("2. Book ticket")
        print("3. View confirmed tickets")
        print("4. Cancel ticket")
        print("5. Cancel a trip (demo/admin)")
        print("6. Exit")
        choice = input("Enter choice: ").strip()
        if choice == "1":
            show_routes(data)
            route_id = input("Enter route ID to view seats (or press Enter to skip): ").strip().upper()
            if route_id in ROUTES:
                show_seats(data, route_id)
        elif choice == "2":
            book_ticket(data)
        elif choice == "3":
            view_tickets(data)
        elif choice == "4":
            cancel_ticket(data)
        elif choice == "5":
            cancel_route(data)
        elif choice == "6":
            print("Thank you for using the Bus Ticket Reservation System.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
