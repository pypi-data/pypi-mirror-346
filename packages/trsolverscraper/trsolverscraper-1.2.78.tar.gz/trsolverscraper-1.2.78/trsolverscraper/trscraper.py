import requests
from .captcha import create_captcha_solver

class TRScraper(requests.Session):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def solve_captcha(self, site, trsolver_api_key, type="trsolver"):
        if not trsolver_api_key:
            raise Exception("TRSolver API anahtarı gerekli")
        solver = create_captcha_solver(trsolver_api_key)
        return solver.solve(site, type)

    # Additional methods here 