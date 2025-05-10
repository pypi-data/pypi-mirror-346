import argparse  # For parsing command line arguments
import logging  # For logging functionality
import sys  # For system-specific parameters and functions
import coloredlogs  # For colored log output

from cert_alert.cert_alert import CertAlert
from cert_alert.config_loader import ConfigLoader


def main():
    # Set up command line argument parser
    parser = argparse.ArgumentParser(description="Certificate Alerter")
    parser.add_argument("--config", default="config.yml", help="Path to config.yml")
    parser.add_argument("--output", default="report.json", help="Path to report.json")
    args = parser.parse_args()

    # Configure logging with colors and set log level to INFO
    coloredlogs.install()
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    try:
        # Load configuration from YAML file via args
        config = ConfigLoader().read_config(args.config)
        
        # Check certificates based on configuration
        report = CertAlert().check_certificates(config)

        # Write report to JSON file
        output = open(args.output, "w")
        output.write(report.model_dump_json(indent=2))
        output.close()

        logger.info(f"✔️ Report written to {args.output}")

        # Exit with error code 1 if any certificate check failed its threshold
        for check in report.checks:
            if check.threshold_reached:
                sys.exit(1)

    except Exception as e:
        # Log any errors and exit with error code
        logger.error(e)
        sys.exit(1)



if __name__ == "__main__":
    main()
