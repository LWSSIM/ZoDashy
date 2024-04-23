#!/usr/bin/env python3
""" instantiate the storage engine """

from backend.models.engine.DB_storage import DB
storage = DB()

storage.reload()
