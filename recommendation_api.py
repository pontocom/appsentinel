from flask import (jsonify, Blueprint, request)
# import databaseConnection as db
import uuid
import datetime
import configparser
import bcrypt
import hashlib
import jwt

recommendation_api = Blueprint('recommendation_api', __name__)