db = db.getSiblingDB("area");

db.area.drop()

db.area.insertMany([
    {
        "id": 1,
        "name": "Graham",
    }, 
    {
        "id": 2,
        "name": "Loic",
    }
])