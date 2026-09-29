# Project Report
## Bus Ticket Reservation System

### 1. Title
Bus Ticket Reservation System

### 2. Problem Statement

A bus company sells seats for several routes and departure times. A passenger selects a route, date, and seat preference. The system must display available seats, prevent double booking, calculate the fare based on the route and passenger category, and issue a ticket. The system must also handle trip cancellation, ticket cancellation, refund deductions based on the time before departure, and payment failure.

### 3. Objectives

1. Provide a simple command-line bus reservation interface.
2. Display available and occupied seats.
3. Prevent two passengers from booking the same seat.
4. Calculate fares for adult, child, and senior passengers.
5. Simulate successful and failed payments.
6. Generate and display a ticket after successful booking.
7. Support ticket cancellation and refund calculation.
8. Handle cancellation of an entire trip.

### 4. Proposed Modules

#### Module 1: Route Management
Stores route names, base fares, and departure times. It also identifies cancelled routes.

#### Module 2: Seat Management
Displays seat availability and checks whether a selected seat is already occupied.

#### Module 3: Fare Calculation
Calculates the final fare according to passenger category.

#### Module 4: Booking Management
Collects passenger details, validates the selected seat, processes payment simulation, and creates a booking.

#### Module 5: Ticket Generation
Creates a unique ticket ID and displays the passenger, route, seat, fare, and ticket status.

#### Module 6: Cancellation and Refund
Cancels a ticket and calculates the refund according to the time remaining before departure.

#### Module 7: Payment Handling
Simulates payment success or failure. A failed payment does not create a ticket.

#### Module 8: Data Storage
Stores booking and cancellation information in a local JSON file so that data remains available after the program is closed.

### 5. Assumptions

- The demonstration system contains three sample routes.
- Each route contains 20 seats.
- Adult passengers pay the base fare.
- Child passengers receive a 30% discount.
- Senior passengers receive a 20% discount.
- Payment is simulated and does not connect to a real bank or payment gateway.
- Refund deductions are project-level assumptions: 10%, 25%, and 50% according to the remaining time.

### 6. Input

The user can enter:
- Route ID
- Seat number
- Passenger name
- Passenger category
- Payment method
- Payment success/failure choice
- Ticket ID for cancellation

### 7. Output

The system displays:
- Available routes
- Seat status
- Calculated fare
- Payment result
- Generated ticket
- Cancellation and refund information
- Error messages for invalid or unavailable selections

### 8. Required Case Handling

| Case | System Behaviour |
|---|---|
| Occupied seat | Rejects the booking and prevents double booking |
| Child fare | Applies child discount |
| Senior fare | Applies senior discount |
| Cancelled trip | Prevents new bookings for the route |
| Cancellation after departure | No refund is issued |
| Payment failure | Ticket is not created and seat remains available |

### 9. Algorithm

1. Load stored booking data.
2. Display the main menu.
3. Let the user select a route.
4. Check whether the route is cancelled.
5. Display available seats.
6. Validate the selected seat.
7. Read passenger category and calculate fare.
8. Simulate payment.
9. If payment fails, stop booking without reserving the seat.
10. If payment succeeds, create a ticket and save the booking.
11. For cancellation, find the ticket and calculate the refund based on the time before departure.
12. Save the updated data.
13. Continue until the user exits.

### 10. Conclusion

The Bus Ticket Reservation System demonstrates basic programming concepts such as functions, conditional statements, loops, lists, dictionaries, file handling, date-time calculations, validation, and modular problem solving. It provides a small command-line model of a real-world reservation system while covering the cases specified in the problem statement.
