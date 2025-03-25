// package myself.custom.asset.controller;
package com.example.controller;


import com.example.model.Seat;
import com.example.service.SeatService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Optional;

@RestController
@RequestMapping("/seats")
@CrossOrigin(origins = "http://localhost:5173")
public class SeatController {

    @Autowired
    private SeatService seatService;

    // Endpoint to get all seats for a flight
    @GetMapping("/flight/{flightID}")
    public List<Seat> getSeatsByFlight(@PathVariable int flightID) {
        return seatService.getSeatsByFlight(flightID); // Get all seats by flightID
    }

    // Endpoint to update the availability of a seat
    @PutMapping("/{flightID}/{seatID}/availability")
    public void updateSeatAvailability(@PathVariable int flightID, @PathVariable String seatID, @RequestParam boolean availability) {
        seatService.updateSeatAvailability(flightID, seatID, availability); // Update seat availability
    }

    @GetMapping("/{flightID}/{seatID}")
    public Optional<Seat> getSeatById(@PathVariable int flightID, @PathVariable String seatID) {
        return seatService.getSeatById(flightID, seatID);  // Fetch seat by composite key
    }
}
