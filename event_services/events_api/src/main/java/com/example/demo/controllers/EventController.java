package com.example.demo.controllers;

import com.example.demo.models.Event;
import com.example.demo.services.EventService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.media.Content;
import io.swagger.v3.oas.annotations.media.Schema;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;
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
@CrossOrigin(origins = { "http://localhost:5500", "http://frontend:5500","http://salehairum.com" })
public class EventController {

    private static final Logger logger = LoggerFactory.getLogger(EventController.class);

    @Autowired
    private EventService eventService;

    @Operation(summary = "Retrieve all events")
    @ApiResponse(responseCode = "200", description = "List of events", content = @Content(schema = @Schema(implementation = Event.class)))
    @GetMapping
    public List<Event> getAllEvents() {
        logger.info("Fetching all events");
        List<Event> events = eventService.getAllEvents();
        logger.debug("Retrieved {} events", events.size());
        return events;
    }

    @Operation(summary = "Retrieve an event by ID")
    @ApiResponses({
            @ApiResponse(responseCode = "200", description = "Event found", content = @Content(schema = @Schema(implementation = Event.class))),
            @ApiResponse(responseCode = "404", description = "Event not found")
    })
    @GetMapping("/{id}")
    public Event getEventById(@PathVariable int id) {
        logger.info("Fetching event with ID: {}", id);
        Event event = eventService.getEventById(id);
        if (event == null) {
            logger.warn("Event with ID {} not found", id);
            throw new ResponseStatusException(HttpStatus.NOT_FOUND, "Event not found");
        }
        return event;
    }

    @Operation(summary = "Retrieve an event by name")
    @ApiResponses({
            @ApiResponse(responseCode = "200", description = "Event found", content = @Content(schema = @Schema(implementation = Event.class))),
            @ApiResponse(responseCode = "404", description = "Event not found")
    })
    @GetMapping("/name/{name}")
    public Event getEventByName(@PathVariable String name) {
        logger.info("Fetching event with name: {}", name);
        Event event = eventService.getEventByName(name);
        if (event == null) {
            logger.warn("Event with name {} not found", name);
            throw new ResponseStatusException(HttpStatus.NOT_FOUND, "Event not found");
        }
        return event;
    }

    @Operation(summary = "Add a new event")
    @ApiResponse(responseCode = "201", description = "Event created", content = @Content(schema = @Schema(implementation = Event.class)))
    @PostMapping
    public Event addEvent(@RequestBody Event event) {
        logger.info("Adding new event: {}", event);
        return eventService.addEvent(event);
    }

    @Operation(summary = "Delete an event by ID")
    @ApiResponse(responseCode = "200", description = "Event deleted")
    @DeleteMapping("/{id}")
    public void deleteEvent(@PathVariable int id) {
        logger.info("Deleting event with ID: {}", id);
        eventService.deleteEvent(id);
    }

    @Operation(summary = "Get ticket price for an event")
    @ApiResponses({
            @ApiResponse(responseCode = "200", description = "Ticket price retrieved"),
            @ApiResponse(responseCode = "404", description = "Event not found")
    })
    @GetMapping("/{id}/price")
    public double getEventTicketPrice(@PathVariable int id) {
        logger.info("Fetching ticket price for event ID: {}", id);
        Event event = eventService.getEventById(id);
        if (event == null) {
            logger.warn("Event with ID {} not found", id);
            throw new ResponseStatusException(HttpStatus.NOT_FOUND, "Event not found");
        }
        return event.getTicket_price();
    }

    @Operation(summary = "Reserve tickets for an event")
    @ApiResponses({
            @ApiResponse(responseCode = "200", description = "Tickets reserved successfully"),
            @ApiResponse(responseCode = "404", description = "Event not found"),
            @ApiResponse(responseCode = "400", description = "Not enough tickets available")
    })
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
                logger.warn("Not enough tickets available for event ID: {}", id);
                throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "Not enough tickets available");
            }
            event.setnTickets(event.getnTickets() - requestedTickets);
            eventService.updateEvent(event);
            logger.info("Successfully reserved {} tickets for event ID: {}", requestedTickets, id);
        }

        return true;
    }
}
