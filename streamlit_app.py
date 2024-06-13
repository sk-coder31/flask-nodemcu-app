import socket
import json
import streamlit as st

def receive_data_from_nodemcu(server_ip, port):
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Define server address and port
    server_address = (server_ip, port)
    st.write(f"Connecting to {server_address[0]}:{server_address[1]}")

    try:
        # Connect to the NodeMCU server
        sock.connect(server_address)
        st.write("Connected to server")

        data = sock.recv(1024)  # Buffer size of 1024 bytes
        data_dict = json.loads(data.decode('utf-8'))
        incoming_data = data_dict['jav_data']
        time_of_flight = incoming_data['tof']
        angle = incoming_data['angle']
        velocity = incoming_data['velocity']
        distance = incoming_data['distance']
        pressure = incoming_data['pressure']

        # Display values in a nice style using Streamlit components
        st.subheader("Data from NodeMCU")
        st.write(f"Time of Flight: {time_of_flight}")
        st.write(f"Angle Thrown: {angle}")
        st.write(f"Velocity Thrown: {velocity}")
        st.write(f"Distance Covered: {distance}")
        st.write(f"Pressure: {pressure}")

    except Exception as e:
        st.error(f"Error: {e}")

    finally:
        # Close the connection
        st.write("Closing connection")
        sock.close()

# Define Streamlit app
def main():
    st.title("NodeMCU Data Receiver")
    st.sidebar.header("Settings")
    server_ip = st.sidebar.text_input("Enter NodeMCU IP", "192.168.4.1")
    port = st.sidebar.number_input("Enter Port", 81)

    if st.sidebar.button("Connect"):
        receive_data_from_nodemcu(server_ip, port)

if __name__ == "__main__":
    main()
