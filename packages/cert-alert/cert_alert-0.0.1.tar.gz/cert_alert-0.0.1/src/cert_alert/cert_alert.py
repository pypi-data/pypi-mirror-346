import logging  # Import logging for debug and error messages
import ssl  # Import ssl for secure connection handling
from datetime import (  # Import datetime-related classes for time calculations
    datetime,
    timedelta,
    timezone,
)
from urllib.parse import urlparse  # Import urlparse for URL parsing
from cryptography import x509  # Import x509 for certificate handling

from cert_alert.models import Check, Config, Report  # Import models


class CertAlert:
    def __init__(self):
        # Initialize logger for the class
        self.logger = logging.getLogger(__name__)
        self.logger.info("Started")

    @staticmethod
    def check_threshold_reached(
        threshold: timedelta, now: datetime, expiry: datetime
    ) -> tuple[bool, int]:
        # Calculate time difference between now and expiry
        delta = expiry - now
        # Return tuple of (is threshold reached, days until expiry)
        return (delta <= threshold, delta.days)

    def get_expiry_from_pem(self, cert_path: str) -> datetime:
        try:
            # Read PEM certificate file
            f = open(cert_path, "r")
            data = f.read().encode()
            # Parse certificate and get expiry date
            cert = x509.load_pem_x509_certificate(data)
            f.close()
            return cert.not_valid_after_utc
        except FileNotFoundError:
            # Handle missing certificate file
            message = f"❌ Certificate {cert_path} not found"
            self.logger.error(message)
            raise Exception(message)
        except Exception as e:
            # Handle other certificate reading errors
            message = f"❌ Failed to read certificate {cert_path}: {e}"
            self.logger.error(message)
            raise Exception(message)

    def get_expiry_from_url(self, url: str) -> datetime:
        # Ensure URL starts with https://
        if url.startswith("https://") is False:
            url = f"https://{url}"
        try:
            # Parse URL to get hostname and port
            parsed_url = urlparse(url)
            hostname = parsed_url.hostname
            port = parsed_url.port

            
            if hostname is None:
                # Handle invalid hostname
                message = f"❌ Invalid url, could not determine hostname from: {url}"
                self.logger.error(message)
                raise Exception(message)
            
            # Use default HTTPS port if not specified
            if port is None:
                message = f"❌ Invalid url, could not determine port from: {url}"
                self.logger.warning(
                    f"⚠ No ports specified for '{hostname}', using default port 443"
                )
                port = 443
                
            # Get and parse certificate from server
            data = ssl.get_server_certificate((hostname, port))
            cert = x509.load_pem_x509_certificate(data.encode())
            return cert.not_valid_after_utc
        except Exception as e:
            # Handle certificate retrieval errors
            message = f"❌ Failed to read certificate from url {url} : {e}"
            self.logger.error(message)
            raise Exception(message)

    def check_certificates(self, config: Config) -> Report:
        # Initialize report with empty checks list
        report = Report(checks=[])

        for certificate in config.certificates:
            # Get expiry date from URL or PEM file
            expiry_date = (
                self.get_expiry_from_url(certificate.url)
                if certificate.url
                else self.get_expiry_from_pem(certificate.file)
            )

            # Check if certificate is expired
            expired, days_to_expiry = self.check_threshold_reached(
                timedelta(days=certificate.threshold),
                datetime.now(timezone.utc),
                expiry_date,
            )

            # Create check entry for report
            check = Check(
                name=certificate.name,
                days_to_expiry=days_to_expiry,
                threshold_reached=expired,
            )

            # Log warning if certificate reached expiry
            if expired:
                self.logger.warning(
                    f"⚠ Certificate '{certificate.name}' has reaches the expiry threshold"
                )

            # Add check to report
            report.checks.append(check)
        
        return report
