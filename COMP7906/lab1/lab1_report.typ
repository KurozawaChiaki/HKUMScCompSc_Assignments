#align(center, text(19pt)[
  *COMP7906 Introduction to Cyber Security* \
  Lab 1
])
#align(center, text(13pt)[
  ZHANG Hongyi
])


= Q1. Ping

== Is #link("www.google.com") alive?

#image("images/ping_google.png")

*Yes.* #link("www.google.com") is alive.

== Is #link("www.hku.hk") alive?

#image("images/ping_hku_hk.png")

== List at least 4 cases that ping reports “Request timed out”

1. *Destination host is unreachable*: If the destination host or device is offline, it won't respond to the ping request, resulting a timeout.

2. *Firewall blocking ping requests*: Firewalls (on the source, destination, or intermediary networks) may be configured to block ICMP traffic, which includes ping requests and replies. This can also result in the ping request timing out.

3. *Network congestion or routing issue*: Heavy traffic on the network or routing problems can prevent ICMP Echo Request from reaching its destination or the ICMP Echo Reply from returning to the sender on time.

4. *Incorrect IP address or hostname*: If the IP address or hostname entered in the ping command is incorrect or invalid, the request may be sent to a non-existent or wrong destination. If an invalid IP address is used, the network may attempt to route the packet to an unreachable destination, leading to a timeout. If a hostname is used and DNS fails to resolve it to the correct IP address (or resolves to a wrong one), the ping request may be sent to an unreachable or incorrect device, resulting in "Request timed out."


= Q2. Traceroute

== How many hosts between your lab pc to #link("www.google.com")?

#image("images/tracert_google.png", width: 300pt)

There are 10 hosts between my pc and #link("www.google.com").

== How many hosts between your lab pc to #link("www.hku.hk")?

#image("images/tracert_hku_hk.png", width: 300pt)

There are at least 10 hosts between my pc and #link("www.hku.hk"). 

== What is the last host you can access with traceroute to #link("www.hku.hk")?

The last host I can access is 147.8.239.15.


= Q3. Nslookup

== The mail exchange servers of hku.hk

#image("images/nslookup_hku_hk.png", width: 300pt)

== Name servers of hku.hk

#image("images/nslookup_hku_hk_name_server.png", width: 300pt)

== Mail exchange servers of google.com

#image("images/nslookup_google_com_mail.png", width: 300pt)

== Name servers of google.com

#image("images/nslookup_google_com_name_server.png", width: 300pt)

== Are the results the same when using different DNS server?

Here are screenshots of trying commands after setting the DNS as 223.5.5.5 (Aliyun Public DNS):

#image("images/nslookup_different_dns_hku_mail.png", width: 300pt)

#image("images/nslookup_different_dns_hku_nameserver.png", width: 300pt)

#image("images/nslookup_different_dns_google_mail.png", width: 300pt)

#image("images/nslookup_different_dns_google_nameserver.png", width: 300pt)

As we can see, the result didn't change.

== What is the TTL setting in hku.hk domain?

#image("images/nslookup_TTL_hku.png", width: 300pt)

It is easy to see that the TTL setting in hku.hk is 53275 seconds (14 hours 47 mins 55 secs).


= Nmap

== Alive hosts in the network

#image("images/nmap_scan_sn.png", width: 300pt)

=== Their open ports

#image("images/nmap_scan.png", width: 300pt)

== OS of these hosts

Linux:
#image("images/OS_Scan_1.png", width: 300pt)

Windows: 
#image("images/OS_Scan_2.png", width: 300pt)
#image("images/os_scan_4.png", width: 300pt)

iOS:
#image("images/os_scan_3.png", width: 300pt)


= Whois

== Who is the technical contact of hku.hk domain?

#image("images/whois_technical_contact_hku.png", width: 300pt)

== How many email addresses did you find? What are they?

I found 4 email addresses.

#image("images/whois_email_1.png", width: 300pt)
The first one is the domain registrar contact information.

#image("images/whois_email_2.png", width: 300pt)
The second one is the registrant contact information.

#image("images/whois_email_3.png", width: 300pt)
The third one is the administrative contact information.

#image("images/whois_email_4.png", width: 300pt)
The last one is the technical contact information.