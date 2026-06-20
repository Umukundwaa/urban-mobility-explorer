def get_top_zones(data, k=5):

    # Manually find top K zones by trip count

    # copy data into a simple list of dicts
    zones = []
    for item in data:
        zones.append({
            "borough": item["borough"],
            "trip_count": item["trip_count"]
        })

    # manually sort using selection sort
    for i in range(len(zones)):
        max_index = i
        for j in range(i + 1, len(zones)):
            if zones[j]["trip_count"] > zones[max_index]["trip_count"]:
                max_index = j
        zones[i], zones[max_index] = zones[max_index], zones[i]

    # return only the top K
    return zones[:k]

