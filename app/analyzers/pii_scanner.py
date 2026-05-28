import re


EMAIL_PATTERN = r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'

PHONE_PATTERN = r'\b\d{10}\b'


def scan_pii(text: str):

    findings = []

    if re.search(EMAIL_PATTERN, text):
        findings.append("EMAIL")

    if re.search(PHONE_PATTERN, text):
        findings.append("PHONE")

    return findings
