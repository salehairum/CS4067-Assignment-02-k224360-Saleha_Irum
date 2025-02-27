package com.example.demo.repositories;

import com.example.demo.models.Event;
import org.springframework.data.mongodb.repository.MongoRepository;

public interface EventRepository extends MongoRepository<Event, Integer> {
    // Custom query method to find an event by name
    Event findByName(String name);
}
