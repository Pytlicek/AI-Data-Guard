import urllib.request
import urllib.robotparser
import socket
import ssl

# Read domains from domains.txt
with open('domains.txt', 'r') as file:
    domains = [domain.strip() for domain in file.readlines()]

# Read excluded domains from excluded.txt
with open('excluded.txt', 'r') as file:
    excluded_domains = [domain.strip() for domain in file.readlines()]

# Exclude the domains listed in excluded.txt
domains_to_check = [domain for domain in domains if domain not in excluded_domains]
domains_to_check = set(domains_to_check)
print("domains_to_check:", domains_to_check)

# Create an SSL context that doesn't verify the certificate
ssl_context = ssl._create_unverified_context()

timeout_seconds = 1
socket.setdefaulttimeout(timeout_seconds)

# Iterate through each domain
for i, domain in enumerate(domains_to_check):
    try:
        robots_url = f'https://{domain}/robots.txt'  # Use HTTPS
        print("\n\n> Checking Domain:", domain, robots_url, f"({i})")

        rp = urllib.robotparser.RobotFileParser()
        rp.set_url(robots_url)
        rp.read()
        rp_response = rp.can_fetch("gptbot", "/")
        print(">> RP_RESPONSE:", rp_response)

        for domain in rp.entries:
            if 'GPTBot' in domain.useragents:
                print(">>>", domain)
                # for rule in domain.rulelines:
                #     print(">>> RULE:", rule)
    except:
        pass