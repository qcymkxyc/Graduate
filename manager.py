#!/usr/bin/python3
# coding=utf-8
"""
    Create On 
    Create by qcymkxyc
    
"""

import os
from app import create_app,db
from app.models import User,Role,Product,Language
from flask_script import Manager,Shell
from flask_migrate import Migrate,MigrateCommand

app = create_app("default")
manager = Manager(app)
migrate = Migrate(app,db)

def make_shell_context():
    return dict(User = User,Role = Role,Product = Product,Language = Language,db = db,app = app)

manager.add_command("shell",Shell(make_shell_context()))
manager.add_command("db",MigrateCommand)

if __name__ == "__main__":
    manager.run()