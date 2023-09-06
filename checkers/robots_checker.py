import urllib.request
import socket
import ssl

# Create an SSL context that doesn't verify the certificate
ssl_context = ssl._create_unverified_context()

timeout_seconds = 2


def check_robots_domain(domain_name):
    print("Checking Domain:", domain_name)
    robots_url = f'https://{domain_name}/robots.txt'  # Use HTTPS
    print("robots_url:", robots_url)

    check_response = {
        "gptbot_is_allowed": False,
        "gptbot_definition_explicit": False
    }

    # Flags to indicate if we are in the GPTBot section or the wildcard section
    in_gptbot_section = False
    in_wildcard_section = False

    # Fetch the content of robots.txt
    try:
        with urllib.request.urlopen(robots_url, timeout=timeout_seconds,
                                    context=ssl_context) as response:
            lines = response.read().decode().splitlines()

        wildcard_rules = []

        # Iterate through the lines of robots.txt
        for line in lines:
            line = line.strip()
            if line == "User-agent: GPTBot":
                print(f"Checking rules for domain_name: {robots_url}")
                in_gptbot_section = True
                in_wildcard_section = False
            elif line == "User-Agent: *":
                in_wildcard_section = True
                in_gptbot_section = False
            elif line.startswith("User-agent:") and (
                    in_gptbot_section or in_wildcard_section):
                break
            elif in_gptbot_section:
                print(">", line)  # Print the Allow/Disallow lines for GPTBot
            elif in_wildcard_section:
                wildcard_rules.append(line)

        # If no specific rules for GPTBot were found, print the wildcard rules
        # if not in_gptbot_section and wildcard_rules:
        #     print("No specific rules for GPTBot. Applying wildcard rules:")
        #     for rule in wildcard_rules:
        #         print(rule)

    except urllib.error.HTTPError:
        print(f"Failed to fetch robots.txt for {domain_name}")
    except socket.timeout:
        print("Timeout occurred")
    except Exception as e:
        print("An unexpected error occurred:", e)

    if in_gptbot_section:
        check_response['gptbot_is_allowed'] = False
        check_response['gptbot_definition_explicit'] = True
    elif in_wildcard_section:
        check_response['gptbot_is_allowed'] = False
        check_response['gptbot_definition_explicit'] = False
    else:
        check_response['gptbot_is_allowed'] = True
        check_response['gptbot_definition_explicit'] = False
    return check_response
