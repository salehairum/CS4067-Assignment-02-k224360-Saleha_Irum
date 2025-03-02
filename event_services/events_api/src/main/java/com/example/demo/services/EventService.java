package com.example.demo.services;

import com.example.demo.models.Event;
import com.example.demo.repositories.EventRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class EventService {

    @Autowired
    private EventRepository eventRepository;

    @Autowired
    private CounterService counterService; // Used for auto-incrementing IDs

    // Get all events
    public List<Event> getAllEvents() {
        return eventRepository.findAll();
    }

    // Get event by ID
    public Event getEventById(int id) {
        return eventRepository.findById(id).orElse(null);
    }

    // Get event by name
    public Event getEventByName(String name) {
        return eventRepository.findByName(name);
    }

    // Add a new event with an auto-incremented ID
    public Event addEvent(Event event) {
        event.setId(counterService.getNextSequence("eventid")); // Assign auto-incremented ID
        return eventRepository.save(event);
    }

    // Delete an event by ID
    public void deleteEvent(int id) {
        eventRepository.deleteById(id);
    }

    public Event updateEvent(Event event) {
        if (eventRepository.existsById(event.getId())) {
            return eventRepository.save(event); // Save updated event
        }
        return null; // Return null if event doesn't exist
    }
}
