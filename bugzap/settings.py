# Scrapy settings for bugzap project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'bugzap'

SPIDER_MODULES = ['bugzap.spiders']
NEWSPIDER_MODULE = 'bugzap.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'bugzap (+http://www.yourdomain.com)'

# Turn cache on for testing.
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 0 # Set to 0 to never expire

# DELAY between requests to same page.
DOWNLOAD_DELAY = 3    # 250 ms of delay