#!/usr/bin/env python

import os
import warden
from warden import app

port = int(os.environ.get('HTTP_PORT', 8002))
debug = int(os.environ.get('DEBUG', False))
host = os.environ.get('HTTP_HOST', '0.0.0.0')

if __name__ == '__main__':
    os.environ.get('dev')
    app.run(host=host, port=port, debug=debug, threaded=True)
