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
        // Optional<Seat> seatOptional = getSeatById(flightID, seatID);
        // if (seatOptional.isPresent()) {
        //     Seat seat = seatOptional.get();
        //     seat.setAvailability(availability);
        //     seatRepository.save(seat); // Update seat availability in DB
        // }
    }

    public Optional<Seat> getSeatById(int flightID, String seatID) {
        SeatKey seatKey = new SeatKey(seatID, flightID);
        return seatRepository.findById(seatKey);  // Find seat by composite key
    }
}
