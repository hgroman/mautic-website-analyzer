#!/bin/bash
cd /var/www/html/mautic/website-analyzer
source venv/bin/activate
python -m src.main
