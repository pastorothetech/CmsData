import threading
import tkinter as tk
from tkinter import ttk
from datetime import datetime
import time
import openai
import json
import re  # Add this import for regular expression

def on_start():
    try:
        # Initialize the OpenAI API client
        openai.api_key = "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"
        
        # Get data from the Tkinter form
        topics = topic_text.get("1.0", tk.END).strip().split('\n')
        start_date = start_date_entry.get()
        end_date = end_date_entry.get()
        
        # Modified query template
        query_template = 'Please provide only a JSON array with no additional text or comments. Each description must be 3 sentences. List 15 impactful records for the topic "{topic}" starting from {start_date} To {end_date}. The JSON array should contain objects with these attributes: "Topic": "", "Title": "", "Date": "", "Description": "".'

        # Read existing data from the JSON file
        try:
            with open("C:\\Users\\PastorOnTheTech\\Desktop\\New folder\\test.json", "r") as f:
                existing_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error reading file: {e}")
            existing_data = []
        
        # Loop through each topic and fetch data
        for topic in topics:
            query = query_template.format(topic=topic, start_date=start_date, end_date=end_date)
            
            # Construct a conversation array
            conversation = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": query}
            ]
            
            # Make an API call to OpenAI GPT-3.5-turbo-16k model
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo-16k",
                    messages=conversation
                )
            except Exception as e:
                print(f"API call failed: {e}")
                continue
            
# ... (rest of the code)

            # Improved JSON parsing logic
            try:
                historical_data_str = response['choices'][0]['message']['content']
                
                # Use regular expression to extract JSON array
                match = re.search(r'\[.*\]', historical_data_str, re.DOTALL)
                
                if match:
                    # Attempt to correct single quotes to double quotes
                    corrected_str = match.group().replace("'", '"')
                    
                    try:
                        # Load JSON string and ensure Unicode escape sequences are converted
                        historical_data = json.loads(corrected_str.encode('utf-8').decode('unicode_escape'))
                    except json.JSONDecodeError:
                        print(f"Failed to parse corrected data: {corrected_str}")
                        continue
                    
                    if not all(key in historical_data[0] for key in ["Topic", "Title", "Date", "Description"]):
                        print("Invalid data format")
                        continue
                else:
                    print(f"Unexpected data format: {historical_data_str}")
                    continue
            except json.JSONDecodeError as e:
                print(f"Malformed data: {e}")
                continue

# ... (rest of the code)

            
            # Append new data to existing data
            existing_data.extend(historical_data)
            
            # Update the progress log
            progress_log.insert(tk.END, f"Processed topic: {topic}. Data saved.\n")
            progress_log.see(tk.END)
            
            # Write the updated data back to the JSON file after each successful operation
            try:
                with open("C:\\Users\\PastorOnTheTech\\Desktop\\New folder\\test.json", "w") as f:
                    json.dump(existing_data, f, indent=4)
                    f.flush()  # Force write to disk
            except Exception as e:
                print(f"Failed to write to file: {e}")

            # Sleep for 1 minute before the next API call
            time.sleep(3)
    
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


# Initialize Tkinter window
# ... (Your Tkinter initialization code remains the same)
    pass

# Initialize Tkinter window
root = tk.Tk()
root.title("OpenAI Historical Data Fetcher")
root.configure(bg='black')
root.wm_attributes("-alpha", 0.9)  # Transparency

# Styling
large_bold_font = ("Helvetica", 14, "bold")
text_color = 'white'

# Cursor settings
# Cursor settings with white color
cursor_options = {'insertwidth': '2', 'insertofftime': 500, 'insertontime': 500, 'insertbackground': 'white'}



# Create a label and text area for topics
topic_label = ttk.Label(root, text="Enter Topics (one per line):", font=large_bold_font, foreground=text_color, background='black')
topic_label.pack(fill='x', padx=10, pady=5)
topic_text = tk.Text(root, height=10, width=40, font=large_bold_font, bg='black', fg=text_color, **cursor_options)
topic_text.pack(fill='x', padx=10, pady=5)

# Create labels and entry fields for start and end dates
start_date_label = ttk.Label(root, text="Enter Start Date (e.g., 366BC):", font=large_bold_font, foreground=text_color, background='black')
start_date_label.pack(fill='x', padx=10, pady=5)
start_date_entry = tk.Entry(root, font=large_bold_font, bg='black', fg=text_color, **cursor_options)
start_date_entry.pack(fill='x', padx=10, pady=5)

end_date_label = ttk.Label(root, text="Enter End Date (e.g., 2023AD):", font=large_bold_font, foreground=text_color, background='black')
end_date_label.pack(fill='x', padx=10, pady=5)
end_date_entry = tk.Entry(root, font=large_bold_font, bg='black', fg=text_color, **cursor_options)
end_date_entry.pack(fill='x', padx=10, pady=5)

# Create a label and entry field for the query
# query_label = ttk.Label(root, text="Enter Query Template:", font=large_bold_font, foreground=text_color, background='black')
# query_label.pack(fill='x', padx=10, pady=5)
# query_entry = tk.Entry(root, font=large_bold_font, bg='black', fg=text_color, **cursor_options)
# query_entry.pack(fill='x', padx=10, pady=5)

# Create a Start button to initiate the process
start_button = tk.Button(root, text="Start", command=lambda: threading.Thread(target=on_start).start())
start_button.pack(fill='x', padx=10, pady=5)

# Create a text widget for the progress log
progress_log = tk.Text(root, height=10, width=60, font=large_bold_font, bg='black', fg=text_color, **cursor_options)
progress_log.pack(fill='x', padx=10, pady=5)

root.mainloop()