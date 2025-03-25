package com.example.model;

import java.io.Serializable;

public class SeatKey implements Serializable {

    private String seatID;
    private int flightID;

    // Default constructor
    public SeatKey() {}

    // Constructor
    public SeatKey(String seatID, int flightID) {
        this.seatID = seatID;
        this.flightID = flightID;
    }

    // Getters and Setters
    public String getSeatID() {
        return seatID;
    }

    public void setSeatID(String seatID) {
        this.seatID = seatID;
    }

    public int getFlightID() {
        return flightID;
    }

    public void setFlightID(int flightID) {
        this.flightID = flightID;
    }

    // Override equals() and hashCode() methods for composite key handling
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;

        SeatKey seatKey = (SeatKey) o;

        if (flightID != seatKey.flightID) return false;
        return seatID.equals(seatKey.seatID);
    }

    @Override
    public int hashCode() {
        int result = seatID.hashCode();
        result = 31 * result + flightID;
        return result;
    }
}
