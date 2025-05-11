from scraipe_cyber.ukraine.cert_ua_scraper import CertUaScraper
from scraipe.defaults import MultiScraper, IngressRule, TextScraper
from scraipe.extended import TelegramMessageScraper, NewsScraper
from scraipe import IScraper

class UkraineCyberMultiScraper(MultiScraper):
    """Multi-scraper that aggregates various scraping strategies for Ukrainian cyber incidents.

    This class combines several specific scrapers including CertUaScraper, an optionally provided 
    Telegram message scraper, a fallback NewsScraper, and a TextScraper. The aggregated ingress rules 
    allow comprehensive coverage of cyber incident data related to Ukraine.

    Attributes:
        None
    """

    def __init__(
        self, 
        telegram_message_scraper: IScraper,
        debug: bool = False, 
        debug_delimiter: str = "; "
    ):
        """Initializes the UkraineCyberMultiScraper with specific scraping components.

        This method sets up a collection of ingress rules that determine the order in which 
        different scrapers are invoked. The Telegram message scraper is applied exclusively if provided.

        Args:
            telegram_message_scraper (IScraper): An instance responsible for scraping Telegram messages.
            debug (bool, optional): If True, activates detailed debugging output. Defaults to False.
            debug_delimiter (str, optional): Delimiter used for separating debug messages. Defaults to "; ".

        Returns:
            None
        """
                
        # Define the ingress rules for the scraper
        ingress_rules = [
            # Cert-UA article scraper 
            IngressRule.from_scraper(CertUaScraper(), exclusive=True),
            # Telegram message scraper if provided
            IngressRule.from_scraper(telegram_message_scraper, exclusive=True) if telegram_message_scraper else None,
            # Fallback to NewsScraper
            IngressRule.from_scraper(NewsScraper()),
            # Fallback to TextScraper
            IngressRule.from_scraper(TextScraper()),
        ]
        
        super().__init__(
            ingress_rules=ingress_rules,
            debug=debug,
            debug_delimiter=debug_delimiter)