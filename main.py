import streamlit as st
import json
from profiles import create_profile, get_notes, get_profile
from ai import ask_ai, get_macros
from form_submit import update_personal_info, add_note, delete_note

st.title("Personal Fitness Tool")

def personal_data_form():
    with st.form("personal_data"):
        st.header("Personal Data")
        
        profile = st.session_state.profile
        name = st.text_input("Name", value=profile.get("name", ""))
        age = st.number_input("Age", min_value=1, max_value=120, step=1, value=int(profile.get("age", 30)))
        weight = st.number_input(
            "Weight (kg)", min_value=0.0, max_value=300.0, step=0.1, value=float(profile.get("weight", 60))
        )
        height = st.number_input(
            "Height (cm)", min_value=0.0, max_value=250.0, step=0.1, value=float(profile.get("height", 165))
        )
        genders = ["Male", "Female", "Other"]
        gender = st.radio("Gender", genders, index=genders.index(profile.get("gender", "Male")))
        activities = ("Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Super Active")
        activity_level = st.selectbox(
            "Activity Level", activities, index=activities.index(profile.get("activity_level", "Sedentary"))
        )
        personal_data_submit = st.form_submit_button("Save")
        
        if personal_data_submit:
            if all([name, age, weight, height, gender, activity_level]):
                with st.spinner():
                    st.session_state.profile = update_personal_info(
                        profile, update_type="general", name=name, weight=weight, height=height,
                        gender=gender, age=age, activity_level=activity_level
                    )
                    st.success("Information saved.")
            else:
                st.warning("Please fill in all of the data!")

def goals_form():
    profile = st.session_state.profile
    with st.form("goals_form"):
        st.header("Goals")
        goal_options = ["Muscle Gain", "Fat Loss", "Stay Active"]
        stored_goals = profile.get("goals", "Muscle Gain")
        default_goals = [g for g in stored_goals.split(",") if g in goal_options] if stored_goals else ["Muscle Gain"]
        goals = st.multiselect("Select your Goals", goal_options, default=default_goals)
        goals_submit = st.form_submit_button("Save")
        if goals_submit:
            if goals:
                with st.spinner():
                    st.session_state.profile = update_personal_info(
                        profile, update_type="goals", goals=",".join(goals)
                    )
                    st.success("Goals updated")
            else:
                st.warning("Please select at least one goal.")

def macros():
    profile = st.session_state.profile
    nutrition = st.container(border=True)
    nutrition.header("Macros")
    
    if nutrition.button("Generate with AI"):
        try:
            # Convert profile dict to a string for the flow
            profile_str = (
                f"Age: {profile['age']}, Weight: {profile['weight']}kg, "
                f"Height: {profile['height']}cm, Gender: {profile['gender']}, "
                f"Activity Level: {profile['activity_level']}"
            )
            goals_str = profile.get("goals", "Muscle Gain")
            with st.spinner("Generating macros with AI..."):
                result = get_macros(profile_str, goals_str)
                if isinstance(result, str):  # If it's a string, convert it to a dictionary
                     result = json.loads(result)
                st.session_state.profile = update_personal_info(
                    profile,
                    update_type="nutrition",
                    calories=result["calories"],
                    protein=result["protein"],
                    fat=result["fat"],
                    carbs=result["carbs"]
                )
                nutrition.success("AI has generated the results.")
        except Exception as e:
            nutrition.error(f"Failed to generate macros: {str(e)}")

    with nutrition.form("nutrition_form", border=False):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            calories = st.number_input(
                "Calories", min_value=0, step=1, value=int(profile.get("calories", 0)),
            )
        with col2:
            protein = st.number_input(
                "Protein", min_value=0, step=1, value=int(profile.get("protein", 0)),
            )
        with col3:
            fat = st.number_input(
                "Fat", min_value=0, step=1, value=int(profile.get("fat", 0)),
            )
        with col4:
            carbs = st.number_input(
                "Carbs", min_value=0, step=1, value=int(profile.get("carbs", 0)),
            )
        if st.form_submit_button("Save"):
            with st.spinner():
                st.session_state.profile = update_personal_info(
                    profile,
                    update_type="nutrition",
                    calories=calories,
                    protein=protein,
                    fat=fat,
                    carbs=carbs,
                )
                st.success("Information saved")

def notes():
    st.subheader("Notes:")
    # Display existing notes
    for i, note in enumerate(st.session_state.notes):
        cols = st.columns([5, 1])
        with cols[0]:
            st.text(note.get("text", "No text"))
        with cols[1]:
            # Use note's 'id' (not '_id') as per form_submit.py
            #if st.button("Delete", key=i):
            #    delete_note(note.get("id"))
            #    st.session_state.notes.pop(i)
            #    st.rerun()
            if st.button("Delete", key=f"delete_{i}"):  # Unique key
                try:
                    delete_note(note.get("id"))
                    st.session_state.notes.pop(i)  # Remove from in-memory list
                    # No rerun; let Streamlit re-render naturally
                except Exception as e:
                    st.error(f"Deletion failed: {str(e)}")
    
    # Add new note
    new_note = st.text_input("Add a new note:")
    if st.button("Add Note"):
        if new_note:
            note = add_note(new_note, st.session_state.profile_id)
            st.session_state.notes.append(note)  # Append the full note dict
            st.rerun()

def ask_ai_func():
    st.subheader("Ask AI")
    user_question = st.text_input("Ask AI a question:")
    if st.button("Ask AI"):
        if user_question:
            with st.spinner("Getting AI response..."):
                profile = st.session_state.profile
                notes = st.session_state.notes
                
                # Build profile string with only user-provided data
                profile_parts = []
                if "name" in profile:
                    profile_parts.append(f"Name: {profile['name']}")
                if "age" in profile:
                    profile_parts.append(f"Age: {profile['age']}")
                if "weight" in profile:
                    profile_parts.append(f"Weight: {profile['weight']}kg")
                if "height" in profile:
                    profile_parts.append(f"Height: {profile['height']}cm")
                if "gender" in profile:
                    profile_parts.append(f"Gender: {profile['gender']}")
                if "activity_level" in profile:
                    profile_parts.append(f"Activity Level: {profile['activity_level']}")
                if "goals" in profile:
                    profile_parts.append(f"Goals: {profile['goals']}")
                if "calories" in profile:
                    profile_parts.append(f"Calories: {profile['calories']}")
                if "protein" in profile:
                    profile_parts.append(f"Protein: {profile['protein']}g")
                if "fat" in profile:
                    profile_parts.append(f"Fat: {profile['fat']}g")
                if "carbs" in profile:
                    profile_parts.append(f"Carbs: {profile['carbs']}g")
                
                # Notes, consistent with notes() function
                notes_str = ""
                if notes:
                    notes_str = "Notes: " + "; ".join([note.get("text", "") for note in notes])
                
                # Combine profile and notes
                full_profile = ", ".join(profile_parts) + (", " + notes_str if notes_str else "")
                if not full_profile:
                    full_profile = "No user data provided yet."
                
                try:
                    result = ask_ai(full_profile, user_question)
                    st.write("AI Response:", result)
                except Exception as e:
                    st.error(f"AI request failed: {str(e)}")
                    st.write("Debug full profile:", full_profile)
        else:
            st.warning("Please enter a question!")


def forms(): 
    if "profile_id" not in st.session_state:
        st.session_state.profile_id = "1"
    
    print("Session State before calling get_profile:", st.session_state)
    
    if "profile" not in st.session_state:
        print(f"Fetching profile for profile_id: {st.session_state.profile_id}")
        profile = get_profile(st.session_state.profile_id)
        if not profile:
            new_profile_id, profile = create_profile(st.session_state.profile_id)
            st.session_state.profile_id = new_profile_id
        st.session_state.profile = profile

    if "notes" not in st.session_state:
        st.session_state.notes = get_notes(st.session_state.profile_id)


    personal_data_form()
    goals_form()
    macros()
    notes()
    ask_ai_func()


if __name__ == "__main__":
    forms()
