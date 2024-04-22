#!/usr/bin/env python3
""" instantiate the storage engine """

from models.engine.DB_storage import DB
storage = DB()

storage.reload()
