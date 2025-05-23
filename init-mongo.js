db = db.getSiblingDB("event_services");  // Change to your database name

db.createCollection("events");

db.createCollection("counters");

db.counters.insertOne({ _id: "eventid", seq: 0 });

function getNextSequence(name) {
    var counter = db.counters.findOneAndUpdate(
        { _id: name },
        { $inc: { seq: 1 } },
        { returnDocument: "after" }
    );
    return counter.seq;
}

db.events.insertMany([
    {
        "_id": getNextSequence("eventid"),
        "name": 'Tech Conference 2025',
        "location": 'Islamabad',
        "date": '10/10/2025',
        "nTickets": 13,
        "ticket_price": 500
    },
    {
        "_id": getNextSequence("eventid"),
        "name": 'AI Summit 2025',
        "location": 'Lahore',
        "date": '15/11/2025',
        "nTickets": 25,
        "ticket_price": 500
    },
    {
        "_id"   : getNextSequence("eventid"),
        "name": 'Game Dev Conference 2025',
        "location": 'Karachi',
        "date": '06/18/2025',
        "nTickets": 71,
        "ticket_price": 500,
    }
]);


db = db.getSiblingDB("notification_service");  // Change to your database name

db.createCollection("notification");
