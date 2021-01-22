import logging
import time
from functools import wraps


class RetryDecorator:
    """
    This class is used to retry requests at an API/Web page.
    if a request fails, it will retry the request while creating exponential timer between each retry and will print
    the reason the requests failed
    """
    logger = logging.getLogger(__name__)  # get the default logger

    @classmethod
    def main(cls, exceptions, total_tries=4, initial_wait=0.5, backoff=2, logger=None):
        """
        calling the decorated function applying an exponential backoff.

        exceptions: Exception(s) that trigger a retry, can be a tuple
        total_tries: Total tries
        initial_wait: Time to first retry
        backoff: Backoff multiplier (e.g. value of 2 will double the delay each retry).
        logger: logger to be used, if none specified print
        """

        def retry_decorator(func):
            @wraps(func)
            def retries(*args, **kwargs):
                tries, delay = total_tries + 1, initial_wait
                while tries > 1:
                    try:
                        # log in the entry and increment the tries count
                        cls.log(f'{total_tries + 2 - tries}. try:', logger)
                        return func(*args, **kwargs)  # if successful return the given function
                    except exceptions as e:
                        tries -= 1
                        print_args = args if args else 'no args'
                        if tries == 1:
                            msg = str(f'Function: {func.__name__}\n'  # print the function's name
                                      # print tries count
                                      f'Failed despite best efforts after {total_tries} tries.\n'
                                      f'args: {print_args}, kwargs: {kwargs}')
                            # log the tries
                            cls.log(msg, logger)
                            raise
                        msg = str(f'Function: {func.__name__}\n'
                                  # arguments passed in and errors
                                  f'Exception: {e}\n'
                                  f'Retrying in {delay} seconds!, args: {print_args}, kwargs: {kwargs}\n')
                        # log the tries
                        cls.log(msg, logger)
                        # try again after the set delay
                        time.sleep(delay)
                        # multiply the delay by the backoff
                        delay *= backoff

            return retries

        return retry_decorator

    @classmethod
    def log(cls, msg, logger=None):
        """
        This method logs in the data to default logger in the config
        """
        if logger:
            logger.warning(msg)
        print(msg)

    def __call__(self, *args, **kwargs):
        return self.main(Exception, logger=self.logger)


retry_requests_decorator = RetryDecorator()()
