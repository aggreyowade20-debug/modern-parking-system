# modern-parking-system

A web-based parking management system for managing parking spaces, vehicles, and parking records.

# Modern Parking System - Kenya

## a) Algorithms for Each Module

- **Slot Display Module:** Iterates through slot keys in $O(N)$ time complexity to return current availability mapping.
- **Vehicle Entry Module:** Converts plate to uppercase, checks active records via Hash Map ($O(1)$ time complexity), performs a Linear Search ($O(N)$) to find the first available slot, registers the entry timestamp, and triggers the entry barrier.
- **Vehicle Exit & Fee Calculation Module:** Looks up the active vehicle in $O(1)$ time, calculates parking duration, computes the fee based on Kenyan Shillings (KES: $\max(\text{Base Fee}, \text{Hours} \times \text{Rate})$), frees up the slot, and triggers the exit barrier.

## b) Data Structures & Reasons for Use

- **Dictionary / Hash Map (`active_vehicles`):** Provides $O(1)$ constant time complexity for searching, inserting, and deleting vehicle records during high-traffic operations.
- **Dictionary / Array Map (`parking_slots`):** Maps each slot ID directly to its occupancy status, enabling fast random access and sequential display rendering on the frontend grid.

## c) Dynamic Database Design (Schema Concept)

- **Table 1: `Slots`**
  - `slot_id` (Primary Key)
  - `status` (Available / Occupied)
- **Table 2: `Vehicles`**
  - `plate_number` (Primary Key)
  - `vehicle_type`
- **Table 3: `ParkingLogs`**
  - `log_id` (Primary Key)
  - `plate_number` (Foreign Key)
  - `slot_id` (Foreign Key)
  - `entry_time`, `exit_time`, `total_fee_kes`, `payment_status`
