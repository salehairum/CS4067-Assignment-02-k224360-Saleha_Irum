package com.example.demo.models;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

@Document(collection = "counters") // This model represents the counters collection in MongoDB
public class Counter {
    @Id
    private String id; // stores "eventid"
    private int seq;

    // Constructors
    public Counter() {
    }

    public Counter(String id, int seq) {
        this.id = id;
        this.seq = seq;
    }

    // Getters and Setters
    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public int getSeq() {
        return seq;
    }

    public void setSeq(int seq) {
        this.seq = seq;
    }
}
