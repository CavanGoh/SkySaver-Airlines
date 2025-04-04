// package myself.custom.asset.service;
package com.example.service;


import com.example.model.Seat;
import com.example.model.SeatKey;
import com.example.repo.SeatRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.Optional;
import java.util.List;

@Service
public class SeatService {

    @Autowired
    private SeatRepository seatRepository;

    public List<Seat> getSeatsByFlight(int flightID) {
        return seatRepository.findByFlightID(flightID); // Fetch seats by flightID
    }

    // Method to update seat availability
    public void updateSeatAvailability(int flightID, String seatID, boolean availability) {
        SeatKey seatKey = new SeatKey(seatID, flightID); // Create composite key from flightID and seatID
        Optional<Seat> seatOptional = seatRepository.findById(seatKey); // Find the seat by composite key

        if (seatOptional.isPresent()) {
            Seat seat = seatOptional.get(); // Get the seat from the result
            seat.setAvailability(availability); // Set the new availability status
            seatRepository.save(seat); // Save the updated seat in the repository (this updates the database)
        } else {
            throw new RuntimeException("Seat not found for the provided flight and seat ID.");
        }
    }

    public Optional<Seat> getSeatById(int flightID, String seatID) {
        SeatKey seatKey = new SeatKey(seatID, flightID);
        return seatRepository.findById(seatKey);  // Find seat by composite key
    }
}
