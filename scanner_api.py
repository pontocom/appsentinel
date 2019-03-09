from flask import (jsonify, Blueprint, request)
# import databaseConnection as db
import uuid
import datetime
import configparser
import bcrypt
import hashlib
import jwt

scanner_api = Blueprint('scanner_api', __name__)