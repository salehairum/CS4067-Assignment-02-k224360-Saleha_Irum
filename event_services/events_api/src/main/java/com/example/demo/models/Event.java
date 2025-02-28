package com.example.demo.models;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

@Document(collection = "events") // Specifies event collection
public class Event {
    @Id
    private String id;
    private String name;
    private String location;
    private String date;
    private int nTickets;
    private double ticket_price; // Renamed field

    // Constructors
    public Event() {
    }

    public Event(String name, String location, String date, int nTickets, double ticket_price) {
        this.name = name;
        this.location = location;
        this.date = date;
        this.nTickets = nTickets;
        this.ticket_price = ticket_price;
    }

    // Getters and Setters
    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getLocation() {
        return location;
    }

    public void setLocation(String location) {
        this.location = location;
    }

    public String getDate() {
        return date;
    }

    public void setDate(String date) {
        this.date = date;
    }

    public int getnTickets() {
        return nTickets;
    }

    public void setnTickets(int nTickets) {
        this.nTickets = nTickets;
    }

    public double getTicket_price() {
        return ticket_price;
    }

    public void setTicket_price(double ticket_price) {
        this.ticket_price = ticket_price;
    }
}
