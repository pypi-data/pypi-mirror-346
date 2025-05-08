import requests
import logging
from entities import Invoice

BASE_URL = "https://pay.deploily.cloud/api/v1"

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ttk_epay:
    """
    A class to represent the ttk_epay application.
    """

    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update(
            {"Accept": "*/*", "Content-Type": "application/json"}
        )

    def get_invoices(self, page_number: int = 1, page_size: int = 10):
        """
        Fetch a list of invoices with pagination.
        """
        url = f"{self.base_url}/admin/invoices"
        params = {"pageNumber": page_number, "pageSize": page_size}
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            return data
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error occurred: {e}")
            logger.error(f"Response status code: {response.status_code}")
            logger.error(f"Response body: {response.text}")
            raise

    def create_invoice(self, invoice_data: Invoice) -> dict:
        """
        Create a new invoice.

        Args:
            invoice_data (Invoice): Invoice object.

        Returns:
            dict: API response as a dictionary.
        """
        url = f"{self.base_url}/admin/invoices"
        try:
            response = self.session.post(url, json=invoice_data.__dict__)
            response.raise_for_status()
            data = response.json()
            return data
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error occurred: {e}")
            logger.error(f"Response status code: {response.status_code}")
            logger.error(f"Response body: {response.text}")
            raise
    
if __name__ == "__main__":
    
    ttk_client = ttk_epay()

    # Get invoices
    logger.info("Fetching invoices...")
    try:
        invoices = ttk_client.get_invoices()
        logger.info(f"Invoices: {invoices}")
    except Exception as e:
        logger.error(f"Failed to fetch invoices: {e}")

    # Create a new invoice
    logger.info("\nCreating new invoice...")
    try:
        # Create a dummy invoice with minimum required fields
        new_invoice = Invoice(ID=1, INVOICE_NUMBER=12345, IS_PAID=False)
        created_invoice = ttk_client.create_invoice(new_invoice)
        logger.info(f"Created invoice: {created_invoice}")
    except Exception as e:
        logger.error(f"Failed to create invoice: {e}")
