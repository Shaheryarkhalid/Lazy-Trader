#! /bin/sh


find . -type f -name '*.py' -not -path '*venv*' -not -path '*pycache*' -not -path '*junk*' -exec wc -l {} +
