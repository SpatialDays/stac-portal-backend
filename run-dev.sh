#!/bin/bash
FLASK_DEBUG=1 FLASK_APP=manage.py FLASK_ENV=dev python3 manage.py run -h 0.0.0.0 -p 5000
