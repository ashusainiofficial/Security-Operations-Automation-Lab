from scapy.all import sniff, IP, TCP

print("=== LIVE NETWORK SNIPER ENGAGED ===")
print("[ MONITORING ] Capturing raw packets moving through your network card...")

def process_packet(packet):
    #Check if the captured packet contains an IP Layer
    if packet.haslayer(IP):
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
        
        # Check if the packet is using the TCP transport protocol
        if packet.haslayer(TCP):
            src_port = packet[TCP].sport
            dst_port = packet[TCP].dport
            
            if dst_port == 80 :
                print(f"[UNENCRYPTED HTTP] Traffic detected! {src_ip}:{src_port} -> {dst_ip}:{dst_port}")
            else:
                print(f"[ TRAFFIC] TCP Stream: {src_ip} -> {dst_ip}")
                
# Start the continuous network sniffer loop (captures 10 packets for this test)
sniff(prn=process_packet, count=10)
print("\n[ COMPLETE ] Live sniffing session terminated safely.")