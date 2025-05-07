import logging
from mysharelib import MyShareData
from mysharelib.utils import setup_logger

# Initialize logger
setup_logger()
logger = logging.getLogger(__name__)

# Example usage
logger.info("myshare_lib testing...")

def main():
    yf = MyShareData.from_source('yahoo')
    ak = MyShareData.from_source('akshare')
    result = ak.get_stock_history('000001', '20250421', '20250425')
    print(result)
    rate = ak.get_exchange_rate('USD/CNY')
    print(rate)


if __name__ == "__main__":
    main()
