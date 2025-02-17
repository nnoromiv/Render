#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/happy-again-backend/")

from main import app as application
application.secret_key = 'ioejd938jDSI§2wo2Ä`ü2'