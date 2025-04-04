// package myself.custom.asset.controller;
package com.example.controller;

import org.springframework.http.ResponseEntity;
import com.example.model.Seat;
import com.example.service.SeatService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;
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

    // Passing resource identifiers in the
    // Endpoint to update the availability of a seat
    @PutMapping("/{flightID}/{seatID}/availability")
    public ResponseEntity<Map<String, Object>> updateSeatAvailability(
            @PathVariable int flightID, 
            @PathVariable String seatID, 
            @RequestBody Map<String, Boolean> request) {

        // Get the availability value from the request body
        Boolean availability = request.get("availability");
        
        if (availability != null) {
            // Call the service to update seat availability
            seatService.updateSeatAvailability(flightID, seatID, availability);

            // Create a response body with a success message and status code
            Map<String, Object> response = Map.of(
                    "code", 200,
                    "message", "Seat updated to taken up"
            );

            // Return a ResponseEntity with a 200 OK status and the response body
            return ResponseEntity.ok(response);
        } else {
            // Handle the case where availability is missing or null
            Map<String, Object> errorResponse = Map.of(
                    "code", 400,
                    "message", "Availability is required"
            );
            return ResponseEntity.badRequest().body(errorResponse); // 400 Bad Request
        }
    }

    @GetMapping("/{flightID}/{seatID}")
    public Optional<Seat> getSeatById(@PathVariable int flightID, @PathVariable String seatID) {
        return seatService.getSeatById(flightID, seatID); // Fetch seat by composite key
    }
}
