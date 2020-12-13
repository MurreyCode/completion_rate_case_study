# entry point to start our app
# python imports
import os

# external imports
from tornado import autoreload
from tornado.ioloop import IOLoop

# local imports
from services.app import make_app


# Main function
if __name__ == '__main__':
    # Define application
    config_name = os.getenv('APP_SETTINGS')
    app = make_app(debug=True)
    app.listen(eval(os.getenv('TORNADO_PORT')))
    autoreload.start()
    autoreload.watch(os.path.join(os.path.dirname(__file__), os.getenv('MODELS_PATH')))
    IOLoop.instance().start()
