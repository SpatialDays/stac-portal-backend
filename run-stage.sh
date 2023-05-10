#!/bin/bash
FLASK_APP=manage.py FLASK_ENV=staging python3 manage.py run -h 0.0.0.0 -p 5000 
