"""Simple healthz check,  check this question for the rational
https://stackoverflow.com/questions/43380939/where-does-the-convention-of-using-healthz-for-application-health-checks-come-f
"""


from flask import Blueprint

healthz = Blueprint("healthz", __name__)


@healthz.route("/healthz")
def get_healthz():
    return "OK"
