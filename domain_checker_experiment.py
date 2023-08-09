import urllib.request
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

# Create an SSL context that doesn't verify the certificate
ssl_context = ssl._create_unverified_context()

timeout_seconds = 2

# Iterate through each domain
for domain in domains_to_check:
    print("Checking Domain:", domain)
    robots_url = f'https://{domain}/robots.txt'  # Use HTTPS

    # Fetch the content of robots.txt
    try:
        with urllib.request.urlopen(robots_url, timeout=timeout_seconds, context=ssl_context) as response:
            lines = response.read().decode().splitlines()

        # Flags to indicate if we are in the GPTBot section or the wildcard section
        in_gptbot_section = False
        in_wildcard_section = False
        wildcard_rules = []

        # Iterate through the lines of robots.txt
        for line in lines:
            line = line.strip()
            if line == "User-agent: GPTBot":
                print(f"Checking rules for domain: {robots_url}")
                in_gptbot_section = True
                in_wildcard_section = False
            elif line == "User-Agent: *":
                in_wildcard_section = True
                in_gptbot_section = False
            elif line.startswith("User-agent:") and (in_gptbot_section or in_wildcard_section):
                break
            elif in_gptbot_section:
                print(line)  # Print the Allow/Disallow lines for GPTBot
            elif in_wildcard_section:
                wildcard_rules.append(line)

        # If no specific rules for GPTBot were found, print the wildcard rules
        # if not in_gptbot_section and wildcard_rules:
        #     print("No specific rules for GPTBot. Applying wildcard rules:")
        #     for rule in wildcard_rules:
        #         print(rule)

    except urllib.error.HTTPError:
        print(f"Failed to fetch robots.txt for {domain}")
    except socket.timeout:
        print("Timeout occurred")
    except Exception as e:
        print("An unexpected error occurred:", e)

    # print()  # Print a newline for separation between domains
