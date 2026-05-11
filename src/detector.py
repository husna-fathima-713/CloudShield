from collections import defaultdict


def detect_failed_logins(log_lines):

    failed_attempts = defaultdict(int)

    for line in log_lines:

        parts = line.split()

        if len(parts) < 2:
            continue

        ip = parts[0]
        status = parts[1]

        if status == "LOGIN_FAILED":
            failed_attempts[ip] += 1

    suspicious_ips = []

    for ip, count in failed_attempts.items():

        if count >= 3:
            suspicious_ips.append((ip, count))

    return suspicious_ips