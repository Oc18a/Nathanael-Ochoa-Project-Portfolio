
import json
import requests
import streamlit as st
from openai import OpenAI 

# Streamlit UI code wrapped in main() function
def main():
    
    # JSON file path
    json_path = 'config.json'

    # Load API key from the JSON file
    with open(json_path, "r") as f:
        config = json.load(f)
        api_key = config['api_key']
        MODEL = config['MODEL']
    
    # Client for API call
    client = OpenAI(api_key = api_key)
    
    # Define scheduling rules to embed in the prompt
    scheduling_rule = """
    Follow these scheduling rules:

    - Breaks are 15 minutes long.
    - Lunches are 45 minutes long.
    - Minimize overlap between team member breaks and lunches as much as possible.
    - Schedule breaks no earlier than 2 hours after clock-in.
    - Schedule lunch no later than the 4th hour and 59th minute of work (lunch must occur before the 5th hour).
    - For shifts that are 6 hours or more, schedule a 2nd break between the time the employee returns from lunch 
      and their shift end time.
    - Do not schedule a break for a team member's last 15 minutes of their shift.
    - Lunches are only scheduled when the shift is longer than 5 hours.
    - Shifts that are 4 hours and 59 minutes long or less only get a single break.
    """
    
    # Streamlit UI
    st.set_page_config(page_title = "Employee Break/Lunch Schedule Generator", layout = "wide")
    
    # App title
    st.title("Employee Break/Lunch Schedule Generator")

    # User input for schedule 
    user_input = st.text_area("Enter TM grid:")

    # Button to trigger the model call
    if st.button("Generate Schedule"):
        if user_input:
            # Call OpenAI API directly to generate schedule
            response = client.chat.completions.create(
                model = MODEL,  
                messages = [
                    {"role": "system", "content": f"""
                    You are a model trained to generate break and lunch schedules for employees based on their 
                    shift start and end times. 
                    {scheduling_rule}
                    """},
                    {"role": "user", "content": f"""
                    Here are the shift details for employees scheduled today:
                    {user_input}
    
                    Create a break and lunch schedule for every employee listed above. Use this format:

                    | TM   | shift start - shift end | 1st break | lunch    | 2nd break | 
                    | TM A | XX:XX XM - XX:XX XM  | XX:XX XM  | XX:XX XM | XX:XX XM  |
                    | TM B | XX:XX XM - XX:XX XM  | XX:XX XM  | XX:XX XM | XX:XX XM  |

                    If a lunch or 2nd break is not applicable enter 'NA'.
                    """}
                ],
                max_tokens = 1000
            )
            
            # Extract and display the generated schedule
            generated_schedule = response.choices[0].message.content
            st.subheader("Generated Break/Lunch Schedule:")
            
            # Dislay response line by line
            for line in generated_schedule.splitlines():
                st.write(line)
        else:
            st.error("Please enter the schedule details before generating.")

# Ensure Streamlit app runs only runs when executed as a script
if __name__ == "__main__":
    main()
