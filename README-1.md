# Bus Ticket Reservation System

## 1. Project Overview

The Bus Ticket Reservation System is a command-line Python project for reserving seats on different bus routes.

It allows a passenger to select a route, choose an available seat, select a passenger category, calculate the fare, make a simulated payment, receive a ticket, and cancel a ticket.

The project also handles an occupied seat, child/senior fares, cancelled trips, cancellation deductions, and payment failure.

## 2. Features

- Display multiple bus routes and departure times.
- Display seat availability.
- Prevent double booking of an occupied seat.
- Calculate fare for adult, child, and senior passengers.
- Simulate payment success and payment failure.
- Generate a unique ticket ID.
- View confirmed tickets.
- Cancel a ticket and calculate refund according to the time before departure.
- Cancel a complete trip and mark its confirmed tickets as cancelled.
- Store booking information in a local JSON file.

## 3. Requirements

- Python 3.9 or later
- No external Python packages are required.

## 4. Project Structure

```text
bus_ticket_reservation/
├── main.py
├── data.json       # created automatically after the first save
├── README.md
├── requirements.txt
└── report.md
```

## 5. How to Run

1. Install Python 3.9 or later.
2. Open a terminal in the project folder.
3. Run:

```bash
python main.py
```

On some systems, use:

```bash
python3 main.py
```

4. Use the numbered menu to test the system.

## 6. Testing the Required Cases

### Occupied seat

Book a seat once and try to book the same seat again. The system rejects the second booking.

### Child or senior fare

Select `child` or `senior` as the passenger category. A category-based discount is applied.

### Cancelled trip

Use the trip cancellation option. New bookings for that route are blocked.

### Cancellation after the refund deadline

If cancellation is attempted after the departure time, the system reports that no refund is available.

### Payment failure

Select a payment method and enter `F` at the payment confirmation step. No ticket is created and the seat remains available.

## 7. Fare Rules Used in This Project

- Adult: 100% of base fare
- Child: 30% discount
- Senior: 20% discount

## 8. Refund Rules Used in This Project

- More than 24 hours before departure: 10% deduction
- 6 to 24 hours before departure: 25% deduction
- Less than 6 hours before departure: 50% deduction
- After departure: no refund

These rules are project assumptions used to demonstrate the required cancellation/refund logic.

## 9. Important Note

This is an academic command-line project. Payment is simulated; no real payment gateway is connected.
