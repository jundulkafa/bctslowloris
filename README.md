# 🔬 Bangladesh Cyber Troops — Slowloris : The Most Powerfull  DoS Attack
**Author:** Jundul Kafa

## Description
A unique, multithreaded Low & Slow Denial-of-Service (Slow DoS) exploit against web servers that use vulnerable versions of thread-based web server software (Apache 1.x, Apache 2.x, httpd, etc.). This tool denies typical service to a web server’s legitimate clients by exhausting server resources at the cost of minimal bandwidth at the attacker's end — *using a single system*.

This unique approach uses staggering amounts of concurrently generated HTTP GET requests even while the other sockets are being created and established on-the-go, and is ironically effective against even some of its typical mitigation mechanisms such as poorly implemented reverse proxy servers.

<div align="center">
<img src="https://github.com/jundulkafa/bctslowloris/blob/Images/Example%20Execution.png" >
<p>Example Execution</p>
</div>

This project was created in Python by the **BCT Team** to supplement our final-year research in cybersecurity, titled "Low & Slow: The Evil Twin of DDoS Attacks", an awareness-based project.

#### Web servers tested so far & confirmed as vulnerable:
- Apache 1.x
- Apache 2.x

#### Web servers untested so far & theoretically vulnerable:
- BeeWare WAF
- DenyAll WAF
- dhttpd
- Flask
- GoAhead WebServer
- Trapeze Wireless Web Portal
- WebSense "block pages"

#### Web servers theoretically invulnerable or not completely vulnerable:
- Cherokee
- Cisco CSS
- IIS6.0
- IIS7.0
- lighttpd
- Netscaler
- nginx
- Squid

*You may test these and report them as vulnerable / invulnerable to update this list in the future.*

## Usage
### Relatively "Elegant" Slow DoS Attack (`--wait`)

`python bctslowloris.py --target example.com --port 80 --length 1024 --threads 6000 --wait`

`python bctslowloris.py -x example.com -p 80 -l 1024 -t 6000 -w`

### Blatant GET Flood Attack (`--end`)

`python bctslowloris.py --target example.com --port 80 --length 1024 --threads 10000 --end`

`python bctslowloris.py -x example.com -p 80 -l 1024 -t 10000 -e`

<div align="center">

| Option       | Description                                              |
|-------------|---------------------------------------------------------|
| target (-x)  | Target web server address (IP address or URL)           |
| port (-p)    | Target web server port (eg: 80)                         |
| length (-l)  | Total packet length (eg: 1000)                          |
| threads (-t) | Threads (sockets) to attack with (eg: 6000)             |
| wait (-w)    | Do not terminate requests (relatively elegant slow DoS) |
| end (-e)     | Terminate all requests correctly (blatant GET flood)    |

</div>

## What BCTSlowloris Does
### Using the `--wait` option
1.  The specified number of client-side software threads (`--threads`) are created — these serve as the individual sockets established between the client and server.
2.  *Unterminated* (deliberately incomplete) GET request headers are created to be sent via all these created sockets.
3.  As this large number of sockets is being created and established, the *unterminated* GET requests are concurrently sent to the target web server using whatever sockets are already established presently.
4.  At randomized time intervals, a single byte is added to this unterminated GET request to keep the communication with the server alive. This time interval is a float value within the 0–5 range, and is randomized for each individual socket, for each individual iteration. This interval also aids in attempting to make the attack seem less automated or static, and more "human-like" to a potential monitoring mechanism at the server's end.

    Essentially, each created and established socket sends *unterminated* (deliberately incomplete) GET requests to the target server first. After this, every 0–5 seconds, a *single* arbitrary byte is added to each of these incomplete GET requests of each socket to give the target server an impression of an alive and *still* ongoing connection — like a drip feed. As the server is still "waiting" for all these concurrent requests to *terminate* (complete) correctly, this consumes a single software thread of the server per successfully connected socket (eg: 1,000 server threads for 1,000 successfully connected sockets). Ergo, BCTSlowloris with the `--wait` option attempts at *occupying* as many of the server-side threads—that are explicitly assigned to be serving clients—as possible to disrupt or hinder typical service to a legitimate client.

5.  When a socket dies or a server-side thread is freed up (unoccupied), additional sockets are concurrently created and established to maximize the number of occupied server-side threads.
6.  Steps #4 and #5 remain active until either of the following occurs:
    - The specified length of the request (`--length`) is reached.
    - The script is manually killed.
    - The target server crashes.

<div align="center">
<img src="https://github.com/jundulkafa/bctslowloris/blob/Images/Unterminated.png" >
<p>Sending Unterminated Requests</p>
</div>

### Using the `--end` option
1.  The specified number of client-side software threads (`--threads`) are created — these serve as the individual sockets established between the client and server.
2.  *Terminated* (completed) GET request headers are created to be sent via all these created sockets.
3.  As this large number of sockets is being created and established, the *terminated* GET requests are concurrently sent to the target web server using whatever sockets are already established presently.

    Essentially, each created and established socket sends *terminated* (completed) GET requests to the target server and goes on doing this repeatedly in an attempt to engage as many server-side threads as possible momentarily. If a request is accepted and processed by the target server, even momentarily, it consumes a single software thread of the server per successfully connected socket (eg: 500 server threads for 500 successfully connected sockets). Ergo, BCTSlowloris with the `--end` option attempts at *overwhelming* the target server by blatantly spraying it with meaningless yet *valid* requests to occupy server-side threads and disrupt service to legitimate clients.

4.  When a socket dies or a server-side thread is freed up (unoccupied), additional sockets are concurrently created and established to maximize the number of occupied server-side threads.
5.  Steps #3 and #4 remain active until either of the following occurs:
    - The specified length of the request (`--length`) is reached.
    - The script is manually killed.
    - The target server crashes.

<div align="center">
<img src="https://github.com/jundulkafa/bctslowloris/blob/Images/Terminated.png" >
<p>Sending Terminated Requests</p>
</div>

## Results
When the server-side threads that are explicitly assigned to be serving clients are completely occupied by BCTSlowloris's flood of terminated or unterminated GET requests, a legitimate client would fail to connect with the web server due to an insufficient amount of available threads on the server-side. This will result in the "Waiting for \<target host\>" message as the web browser anticipates a connection but never establishes one:

<div align="center">
<img src="https://github.com/jundulkafa/bctslowloris/blob/Images/Waiting.png" >
<p>Waiting...</p>
</div>

Further, upon waiting for a long enough amount of time, the web browser gives up as the server-side threads are completely occupied serving the attacker's requests. This is when the "ERR_CONNECTION_TIMED_OUT" error message is displayed to a legitimate client attempting to access the web page:

<div align="center">
<img src="https://github.com/jundulkafa/bctslowloris/blob/Images/ERR_CONNECTION_TIMED_OUT.png" >
<p>ERR_CONNECTION_TIMED_OUT</p>
</div>

## Poorly Implemented Reverse Proxy Servers
A reverse proxy server serves as an additional, protective layer to the destination server by obscuring the destination server's direct specifications (such as its IP address). Hence, if a ping command were to be executed using the primary web page domain using `ping webpage.com`, then the IP address being pinged would be that of the *reverse proxy* server instead of the destination web server where the web page exists.

That stated, if a reverse proxy server is poorly implemented or configured, then it would be vulnerable to BCTSlowloris *first*. This means that if the reverse proxy server *itself* is crippled by the attack, then since it serves as the only route through which a user could access the *intended* destination web server, the destination web server would *also* be inaccessible — technically *also* being a denial of typical service.

Upon a reverse proxy server failure such as this, a page resembling the following context / nature would display to a legitimate client attempting to access the web page:

<div align="center">
<img src="https://github.com/jundulkafa/bctslowloris/blob/Images/Reverse%20Proxy%20Failure.jpg" >
<p>Reverse Proxy Server Failure</p>
</div>

## Disclaimer
**BCTSlowloris was created for educational and research purposes only.** The BCT Team provides this tool to raise awareness surrounding the fact that organizations are still using vulnerable web server software versions. We neither endorse nor shall be held responsible for any unethical, unauthorized, or malicious use of this tool. **Unauthorized testing against any network or system without explicit permission is illegal.**

*Use knowledge responsibly and ethically to improve security, not to compromise it.*

## Dependencies
Install the required Python packages via pip:
```bash
pip install colorama termcolor
```

---
**Author:** jundulkafa
**Team:** BCT Team
**Project Link:** https://github.com/jundulkafa/bctslowloris
**Website:** http://jundulkafa.atwebpages.com/
