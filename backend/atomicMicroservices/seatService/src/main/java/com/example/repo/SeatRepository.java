// package myself.custom.asset.repository;
package com.example.repo;


import com.example.model.Seat;
import com.example.model.SeatKey;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface SeatRepository extends JpaRepository<Seat, SeatKey> {
    // Custom query methods can go here, such as:
    List<Seat> findByFlightID(int flightID);
}
