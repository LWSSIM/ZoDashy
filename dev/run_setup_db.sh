#!/usr/bin/bash
# This file is used to run the set_db_psql.py w/ env_vars.sh script
#
# After creation you can run th following command to log in to the database:
# ```
# psql -d zo_db -U zo_dev -W -h localhost -p 5432
# ```

env $(cat env_vars.sh | xargs) python3 set_db_psql.py
