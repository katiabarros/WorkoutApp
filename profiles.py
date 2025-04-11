from db import personal_data_collection, notes_collection

def get_values(_id):
    return {
        "id": str(_id),
        "name": "",
        "age": 30,
        "weight": 60,
        "height": 165,
        "activity_level": "Moderately Active",
        "gender": "Male",
        "goal_1": "Muscle Gain",
        "calories": 2000,
        "protein": 140,
        "fat": 20,
        "carbs": 100,
    }

def create_profile(_id):
    profile_values = get_values(_id)
    personal_data_collection.add(
        ids=[profile_values["id"]],
        metadatas=[profile_values],
        documents=["User profile data"]
    )
    print(f"Created profile with ID: {profile_values['id']}")
    return profile_values["id"], profile_values  # Return both ID and metadata
    #return profile_values["id"], profile_values

def get_profile(profile_id):
    print(f"Fetching profile for ID: {profile_id}")
    results = personal_data_collection.get(ids=[str(profile_id)])
    print(f"Results from database: {results}")
    if not results or "metadatas" not in results or not results["metadatas"]:
        return None
    return results["metadatas"][0]

def get_notes(profile_id):
    """Retrieve all notes for a given profile_id"""
    results = notes_collection.get(where={"user_id": str(profile_id)})
    if results and "metadatas" in results and results["metadatas"]:
        return results["metadatas"]
    return []
