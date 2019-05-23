apt-get update
apt-get install python3-bs4
echo '15   *   *   *   *   python3 /root/scrape/scrape.py >/dev/null 2&>1' >> /etc/crontab
