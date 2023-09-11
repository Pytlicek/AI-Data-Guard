import urllib.robotparser
import urllib.request
import robots
import socket
import ssl

# Create an SSL context that doesn't verify the certificate
ssl_context = ssl._create_unverified_context()
timeout_seconds = 1
socket.setdefaulttimeout(timeout_seconds)


def get_robots_txt_on_tld(domain_name):
    robots_url = f'https://{domain_name}/robots.txt'  # Use HTTPS
    print("Checking Domain:", domain_name, robots_url)

    # Fetch the content of robots.txt
    try:
        with urllib.request.urlopen(robots_url, timeout=timeout_seconds,
                                    context=ssl_context) as response:
            lines = response.read().decode().splitlines()
        return lines

    except urllib.error.HTTPError:
        print(f"Failed to fetch robots.txt for {domain_name}")
    except socket.timeout:
        print("Timeout occurred")
    except Exception as e:
        print("An unexpected error occurred:", e)


def check_robots_domain(domain_name):
    robots_url = f'https://{domain_name}/robots.txt'  # Use HTTPS
    print("Checking Domain:", domain_name, robots_url)

    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(robots_url)
    rp.read()
    rp_response = rp.can_fetch("gptbot", "/")

    check_response = {
        'gptbot_is_allowed': rp_response,
        'gptbot_definition_explicit': False
    }

    for domain in rp.entries:
        if 'GPTBot' in domain.useragents:
            check_response['gptbot_definition_explicit'] = True
            print('GPTBot Rules:')
            for rule in domain.rulelines:
                print("rule:", rule)
    return check_response
