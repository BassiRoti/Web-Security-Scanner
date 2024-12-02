import argparse
import json
import logging
from crawler import Crawler
from vulnerability_scanner import VulnerabilityScanner


def main(target_url, config):
    logging.basicConfig(filename="scan.log", level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    logging.info(f"Starting scan for {target_url}")

    try:
        crawler = Crawler(target_url, delay=config["delay"])
        site_map = crawler.crawl()
        print("Crawl result from sitemap:", site_map)

        with open("report.txt", "w") as report_file:
            report_file.write("Web Vulnerability Scanner Report\n")
            report_file.write(f"Target URL: {target_url}\n")
            report_file.write("Scan Summary:\n\n")

            scanner = VulnerabilityScanner(site_map, report_file)
            scanner.run()


            for url in site_map:
                scanner.check_insecure_headers(url)

        logging.info("Scan completed successfully")

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        print(f"[!] An error occurred: {e}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Web Vulnerability Scanner")
    parser.add_argument("url", help="The target URL to scan")
    args = parser.parse_args()

    with open("config.json") as f:
        config = json.load(f)

    main(args.url, config)
