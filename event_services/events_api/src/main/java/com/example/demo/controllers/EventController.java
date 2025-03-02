//mvn spring-boot:run

package com.example.demo.controllers;

import com.example.demo.models.Event;
import com.example.demo.services.EventService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/events")
@CrossOrigin(origins = "http://127.0.0.1:5500") // Allow frontend requests
public class EventController {

    @Autowired
    private EventService eventService;

    // Get all events
    @GetMapping
    public List<Event> getAllEvents() {
        return eventService.getAllEvents();
    }

    // Get event by ID
    @GetMapping("/{id}")
    public Event getEventById(@PathVariable int id) {
        return eventService.getEventById(id);
    }

    // Get event by name
    @GetMapping("/name/{name}")
    public Event getEventByName(@PathVariable String name) {
        return eventService.getEventByName(name);
    }

    // Add new event
    @PostMapping
    public Event addEvent(@RequestBody Event event) {
        return eventService.addEvent(event);
    }

    // Delete event by ID
    @DeleteMapping("/{id}")
    public void deleteEvent(@PathVariable int id) {
        eventService.deleteEvent(id);
    }

    @GetMapping("/{id}/price")
    public double getEventTicketPrice(@PathVariable int id) {
        Event event = eventService.getEventById(id);
        if (event == null) {
            throw new ResponseStatusException(HttpStatus.NOT_FOUND, "Event not found");
        }
        return event.getTicket_price();
    }

    @PostMapping("/{id}/reserve-tickets")
    public boolean reserveTickets(@PathVariable int id, @RequestBody Map<String, Integer> requestBody) {
        int requestedTickets = requestBody.get("requestedTickets");
        Event event = eventService.getEventById(id);
        if (event == null) {
            throw new ResponseStatusException(HttpStatus.NOT_FOUND, "Event not found");
        }

        synchronized (this) { // Prevent race conditions
            if (event.getnTickets() < requestedTickets) {
                return false; // Not enough tickets
            }

            // Deduct tickets and update event
            event.setnTickets(event.getnTickets() - requestedTickets);
            eventService.updateEvent(event);
        }

        return true; // Booking can proceed
    }

}
