from flask_cors import CORS

from happy_again import create_app
from happy_again import db
from happy_again.apis.utils import Helper
from happy_again.common.consts import deployment
from waitress import serve

# from flask import Flask
# from flask_apscheduler import APScheduler
# from check_inactive_users import checkInactivity
# from checked_users import checkedUsers

app = create_app()
# scheduler = APScheduler()
CORS(app)

print("app created")
db.create_all()

@app.errorhandler(400)
def bad_request(error):
    return Helper.create_error_response(400, "Unexpected Error")

@app.errorhandler(405)
def method_not_allowed(error):
    return Helper.method_not_allowed()

@app.errorhandler(422)
def unprocessable_entity(error):
    return Helper.create_error_response(422, "Unauthorized user: Signature failure")

@app.errorhandler(500)
def internal_server_error(error):
    return Helper.internal_server_error()

if __name__ == "__main__":

    if deployment:
        # scheduler.add_job(id="email_rem", func=check, trigger='cron', hour=11, minute=1)
        # scheduler.add_job(id="checked_users", func=checkedUsers, trigger='interval', seconds=5)
        # scheduler.start()
        serve(app, port=80)
        app.run()
    else:
        # scheduler.add_job(id="email_rem", func=check, trigger='cron', hour=11, minute=1)
        # scheduler.add_job(id="checked_users", func=checkedUsers, trigger='interval', seconds=5)
        # scheduler.start()
        serve(app, port=1234)
        # app.run(port=1234, debug=True)
