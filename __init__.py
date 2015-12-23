from flask_restful import Api, Resource, fields, marshal_with, reqparse
from flask import Flask, jsonify, request, abort, g, session
import  json

from werkzeug.security import check_password_hash, generate_password_hash
from flask.ext.sqlalchemy import SQLAlchemy
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired
from flask.ext.httpauth import *