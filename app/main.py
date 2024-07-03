""" Streamlit app for running a ping command to a destination address. """

import streamlit as st
import subprocess
import platform


def run_ping(host, output_area):
    """
    Runs ping command and updates output area in real-time
    """
    param = "-n" if platform.system().lower() == "windows" else "-c"
    command = ["ping", param, "14", host]

    process = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )

    output = ""
    for line in process.stdout:
        output += line
        output_area.text_area("Console Output", value=output, height=200)

    print(f"Process return code: {process.returncode}")

    return True


def main():
    """Main function of the App."""
    st.title("Destination Address Ping with Console Output")

    destination_address = st.text_input("Enter your destination address:")

    console_output = st.empty()

    if st.button("Run Ping"):
        if destination_address:
            status = st.warning(f"Pinging {destination_address}...")
            console_output.text_area("Console Output", value="", height=200)
            success = run_ping(destination_address, console_output)

            if success:
                status.success(f"Successfully pinged {destination_address}")
            else:
                status.error(f"Failed to ping {destination_address}")
        else:
            status.warning(
                "Please enter a destination address before running the ping."
            )


if __name__ == "__main__":
    main()
