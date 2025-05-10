import abc
import logging
import sys
import requests

if sys.version_info >= (3, 4):
    ABC = abc.ABC  # noqa
else:
    ABC = abc.ABCMeta('ABC', (), {})

# ------------------------------------------------------------------------------- #

captchaSolvers = {}

# ------------------------------------------------------------------------------- #


class Captcha(ABC):
    @abc.abstractmethod
    def __init__(self, name):
        captchaSolvers[name] = self

    # ------------------------------------------------------------------------------- #

    @classmethod
    def dynamicImport(cls, name):
        if name not in captchaSolvers:
            try:
                __import__(f'{cls.__module__}.{name}')
                if not isinstance(captchaSolvers.get(name), Captcha):
                    raise ImportError('The anti captcha provider was not initialized.')
            except ImportError as e:
                sys.tracebacklimit = 0
                logging.error(f'Unable to load {name} anti captcha provider -> {e}')
                raise

        return captchaSolvers[name]

    # ------------------------------------------------------------------------------- #

    @abc.abstractmethod
    def getCaptchaAnswer(self, captchaType, url, siteKey, captchaParams):
        pass

    # ------------------------------------------------------------------------------- #

    def solveCaptcha(self, captchaType, url, siteKey, captchaParams):
        return self.getCaptchaAnswer(captchaType, url, siteKey, captchaParams)

class TRSolverCaptcha:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "http://api.trsolver.com"

    def solve(self, site, type="trsolver"):
        """
        TRSolver API ile captcha çözme
        """
        params = {
            "apikey": self.api_key,
            "site": site
        }
        
        response = requests.get(f"{self.base_url}/get-token", params=params)
        if response.status_code == 200:
            return response.text
        else:
            raise Exception(f"TRSolver API Error: {response.text}")

def create_captcha_solver(api_key):
    return TRSolverCaptcha(api_key)
