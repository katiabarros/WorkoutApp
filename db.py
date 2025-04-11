import chromadb
import streamlit as st
import os

# Database path
DB_PATH = "./chroma_db"

# Ensure the storage directory exists
if not os.path.exists(DB_PATH):
    os.makedirs(DB_PATH)

# Initialize ChromaDB client and collections
@st.cache_resource
def init_chroma_db():
    try:
        # Initialize the persistent client
        client = chromadb.PersistentClient(path=DB_PATH)
        
        # Collection names
        collection_names = ["personal_data", "notes"]
        
        # Create or get collections
        collections = {}
        for name in collection_names:
            collections[name] = client.get_or_create_collection(name=name)
            # Verify collection creation
            collections[name].count()  # Forces table creation if needed
        
        return collections
    except Exception as e:
        st.error(f"Failed to initialize ChromaDB: {str(e)}")
        return None

# Get collections
collections = init_chroma_db()
if collections is None:
    st.error("ChromaDB initialization failed. Check logs for details.")
    st.stop()

# Assign collections
personal_data_collection = collections["personal_data"]
notes_collection = collections["notes"]

# Debug output to confirm initialization
try:
    st.write("ChromaDB initialized. Collections:", 
             {"personal_data": personal_data_collection.count(), 
              "notes": notes_collection.count()})
except Exception as e:
    st.error(f"Error verifying collections: {str(e)}")
