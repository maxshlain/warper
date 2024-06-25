import streamlit as st
import subprocess
import threading
import time

def run_command(command, file_path, output):
    try:
        process = subprocess.Popen(
            f"{command} {file_path}",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            text=True
        )
        
        while True:
            output_line = process.stdout.readline()
            if output_line == '' and process.poll() is not None:
                break
            if output_line:
                output.append(output_line.strip())
                time.sleep(0.1)  # Small delay to prevent excessive updates
        
        for error_line in process.stderr:
            output.append(f"Error: {error_line.strip()}")
    
    except Exception as e:
        output.append(f"Error: {str(e)}")

st.title("Command Execution App")

command = st.text_input("Enter command:", "cat")
file_path = st.text_input("Enter file path:", "/Users/maximshlain/Code/GitHub/warper/requirements.txt")
run_button = st.button("Run")
abort_button = st.button("Abort")
status = st.info("Please enter a command and file path to execute.")

output = st.empty()
output_list = []

if 'thread' not in st.session_state:
    st.session_state.thread = None

if run_button:
    output_list.clear()
    if st.session_state.thread and st.session_state.thread.is_alive():
        st.warning("A command is already running. Please abort it first.")
    else:
        st.session_state.thread = threading.Thread(target=run_command, args=(command, file_path, output_list))
        st.session_state.thread.start()

if abort_button:
    if st.session_state.thread and st.session_state.thread.is_alive():
        st.session_state.thread = None
        st.success("Command execution aborted.")
    else:
        st.warning("No command is currently running.")

if st.session_state.thread and st.session_state.thread.is_alive():
    info = st.info("Command is running...")

# Update output in real-time
while st.session_state.thread and st.session_state.thread.is_alive():
    output.text_area("Output:", value="\n".join(output_list), height=400)
    time.sleep(0.1)  # Small delay to prevent excessive updates

# Final update after thread completion
# output.text_area("Output:", value="\n".join(output_list), height=400)
status.text("Command execution completed.")
