from scapy.all import *
import time

# Custom source IP address and target information
destination_ip = "157.245.243.181"
destination_port = 80

# HTTP POST request payload
username = "badguyrulz4ever"
password = "aDmInAdMiN"

with open("uploaded_files.txt", "r") as f:
    for filename in f:
        filename = filename.strip()
        http_payload = (
            "POST /delete HTTP/1.1\r\n"
            f"Host: {destination_ip}\r\n"
            "User-Agent: Scapy\r\n"
            "Content-Type: application/x-www-form-urlencoded\r\n"
            f"Content-Length: {len(f'username={username}&password={password}&filename={filename}')}\r\n"
            "Connection: close\r\n"
            "\r\n"
            f"username={username}&password={password}&filename={filename}"
        )

        # Create the IP layer
        ip_layer = IP(dst=destination_ip)

        # Retry loop
        retries = 3
        while retries > 0:
            try:
                # Create the TCP layer with random source port
                tcp_layer = TCP(sport=RandShort(), dport=destination_port, flags="S")

                # Create the initial SYN packet
                syn_packet = ip_layer/tcp_layer

                # Send SYN and receive SYN-ACK
                syn_ack_response = sr1(syn_packet, timeout=2)

                if syn_ack_response:
                    # Create the ACK packet for the received SYN-ACK
                    ack_packet = ip_layer/TCP(sport=syn_ack_response.dport, dport=destination_port, seq=syn_ack_response.ack, ack=syn_ack_response.seq + 1, flags="A")

                    # Create the final packet with HTTP POST request
                    post_packet = ip_layer/TCP(sport=syn_ack_response.dport, dport=destination_port, seq=ack_packet.seq, ack=ack_packet.ack, flags="PA")/http_payload

                    # Send the ACK packet
                    send(ack_packet)

                    # Send the POST packet and print the response
                    sr1(post_packet, timeout=2)

                    # Break out of the retry loop on success
                    break
                else:
                    print("No response, retrying...")
                    retries -= 1
                    time.sleep(1)
            except Exception as e:
                print(f"Error: {e}")
                retries -= 1
                time.sleep(1)
