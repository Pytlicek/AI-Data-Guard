from urllib.request import urlopen
import urllib.robotparser
import urllib.request
import tldextract
import robots
import socket
import ssl

# Create an SSL context that doesn't verify the certificate
ssl_context = ssl._create_unverified_context()
timeout_seconds = 2


class TimeoutRobotFileParser(urllib.robotparser.RobotFileParser):
    def read(self, timeout=None):
        """Reads the robots.txt URL and feeds it to the parser."""
        try:
            f = urlopen(self.url, timeout=timeout_seconds)
        except urllib.error.HTTPError as exc:
            if exc.status == 404:
                return
            else:
                raise
        raw = f.read()
        self.parse(raw.decode("utf-8").splitlines())


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


def get_domain_name_from_url(url: str, get_tld: bool = False) -> str:
    extracted_info = tldextract.extract(url)
    if get_tld:
        return extracted_info.registered_domain
    domain = '.'.join(extracted_info)

    # remove leading dot
    if domain.startswith('.'):
        domain = domain[1:]
    return domain


def check_robots_by_url(
        domain_name: str,
        url: str,
        useragent: str = None
) -> dict:
    # socket.setdefaulttimeout(timeout_seconds)
    useragent = useragent or "gptbot"
    robots_url = f'https://{domain_name}/robots.txt'  # Use HTTPS
    print("Checking Domain:", domain_name, robots_url)

    robot_parser = TimeoutRobotFileParser()
    robot_parser.set_url(robots_url)
    robot_parser.read()

    robot_parser_response = robot_parser.can_fetch(useragent, url)

    check_response = {
        'gptbot_is_allowed': robot_parser_response,
        'gptbot_definition_explicit': False
    }

    for domain in robot_parser.entries:
        if 'GPTBot' in domain.useragents:
            check_response['gptbot_definition_explicit'] = True
            print('GPTBot Rules:')
            for rule in domain.rulelines:
                print("rule:", rule)

    return check_response


def check_robots_domain(domain_name: str) -> dict:
    check_response = check_robots_by_url(domain_name, url="/")
    return check_response


def check_robots_url(url: str) -> dict:
    domain_name = get_domain_name_from_url(url)
    check_response = check_robots_by_url(domain_name=domain_name, url=url)
    check_response['domain_name'] = domain_name
    return check_response
