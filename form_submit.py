from db import personal_data_collection, notes_collection
from datetime import datetime
#from chromadb import Client

#client = Client()
#notes_collection = client.get_or_create_collection("notes")

def update_personal_info(existing, update_type, **kwargs):
    """Update personal info in ChromaDB (overwrite approach)"""
    # Ensure 'id' exists
    profile_id = str(existing.get("id", kwargs.get("profile_id", "unknown_id")))

    if update_type == "goals":
        existing["goals"] = kwargs.get("goals", [])
    else:
        existing.update(kwargs)  # Update the flat metadata dictionary

    # Overwrite in ChromaDB
    personal_data_collection.update(
        ids=[profile_id],
        metadatas=[existing],
        documents=["Updated user profile"]
    )
    
    return existing


def add_note(note, profile_id):
    new_note = {
        "id": f"note_{profile_id}_{datetime.now().timestamp()}",
        "user_id": profile_id,
        "text": note,
        "timestamp": datetime.now().isoformat(),
    }
    notes_collection.add(
        ids=[new_note["id"]],
        metadatas=[new_note],
        documents=[note]
    )
    return new_note
    
def delete_note(_id):
    #"""Delete a note in ChromaDB"""
    #notes_collection.delete(ids=[str(_id)])
    #return True  # ChromaDB doesn't return delete status
    """Delete a note in ChromaDB and verify removal"""
    note_id = str(_id)  # Ensure ID is a string
    # Delete the note
    notes_collection.delete(ids=[note_id])
    # Verify deletion by checking if the note still exists
    remaining = notes_collection.get(ids=[note_id])
    print(f"After deletion, remaining: {remaining}")
    if remaining["ids"]:  # If the ID is still present, deletion failed
        raise Exception(f"Failed to delete note with ID: {note_id}")
    return True

