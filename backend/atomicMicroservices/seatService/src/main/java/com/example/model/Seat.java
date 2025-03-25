// package myself.custom.asset.model;
package com.example.model;


import lombok.Getter;
import lombok.Setter;
import lombok.ToString;

import javax.persistence.*;
import java.io.Serializable;

@Entity
@Setter
@Getter
@ToString
@IdClass(SeatKey.class)  // Declare the composite primary key class
public class Seat {

    @Id
    private String seatID;

    @Id
    private int flightID; // Composite key part

    private boolean availability;

}
