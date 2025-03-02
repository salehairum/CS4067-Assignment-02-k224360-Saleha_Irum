package com.example.demo.controllers;

import com.example.demo.models.Event;
import com.example.demo.services.EventService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
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
    
    private static final Logger logger = LoggerFactory.getLogger(EventController.class);
    
    @Autowired
    private EventService eventService;

    // Get all events
    @GetMapping
    public List<Event> getAllEvents() {
        logger.info("Fetching all events");
        List<Event> events = eventService.getAllEvents();
        logger.debug("Retrieved {} events", events.size());
        return events;
    }

    // Get event by ID
    @GetMapping("/{id}")
    public Event getEventById(@PathVariable int id) {
        logger.info("Fetching event with ID: {}", id);
        Event event = eventService.getEventById(id);
        if (event == null) {
            logger.warn("Event with ID {} not found", id);
            throw new ResponseStatusException(HttpStatus.NOT_FOUND, "Event not found");
        }
        logger.debug("Event retrieved: {}", event);
        return event;
    }

    // Get event by name
    @GetMapping("/name/{name}")
    public Event getEventByName(@PathVariable String name) {
        logger.info("Fetching event with name: {}", name);
        Event event = eventService.getEventByName(name);
        if (event == null) {
            logger.warn("Event with name {} not found", name);
            throw new ResponseStatusException(HttpStatus.NOT_FOUND, "Event not found");
        }
        logger.debug("Event retrieved: {}", event);
        return event;
    }

    // Add new event
    @PostMapping
    public Event addEvent(@RequestBody Event event) {
        logger.info("Adding new event: {}", event);
        Event createdEvent = eventService.addEvent(event);
        logger.debug("Event added successfully: {}", createdEvent);
        return createdEvent;
    }

    // Delete event by ID
    @DeleteMapping("/{id}")
    public void deleteEvent(@PathVariable int id) {
        logger.info("Deleting event with ID: {}", id);
        eventService.deleteEvent(id);
        logger.debug("Event with ID {} deleted successfully", id);
    }

    @GetMapping("/{id}/price")
    public double getEventTicketPrice(@PathVariable int id) {
        logger.info("Fetching ticket price for event ID: {}", id);
        Event event = eventService.getEventById(id);
        if (event == null) {
            logger.warn("Event with ID {} not found", id);
            throw new ResponseStatusException(HttpStatus.NOT_FOUND, "Event not found");
        }
        double price = event.getTicket_price();
        logger.debug("Ticket price for event {}: {}", id, price);
        return price;
    }

    @PostMapping("/{id}/reserve-tickets")
    public boolean reserveTickets(@PathVariable int id, @RequestBody Map<String, Integer> requestBody) {
        int requestedTickets = requestBody.get("requestedTickets");
        logger.info("Reserving {} tickets for event ID: {}", requestedTickets, id);
        
        Event event = eventService.getEventById(id);
        if (event == null) {
            logger.warn("Event with ID {} not found", id);
            throw new ResponseStatusException(HttpStatus.NOT_FOUND, "Event not found");
        }

        synchronized (this) { // Prevent race conditions
            if (event.getnTickets() < requestedTickets) {
                logger.warn("Not enough tickets available for event ID: {}. Requested: {}, Available: {}", id, requestedTickets, event.getnTickets());
                return false;
            }

            // Deduct tickets and update event
            event.setnTickets(event.getnTickets() - requestedTickets);
            eventService.updateEvent(event);
            logger.info("Successfully reserved {} tickets for event ID: {}", requestedTickets, id);
        }

        return true; // Booking can proceed
    }
}
