from flask import Blueprint

blueprint=Blueprint(
    'threats_blueprint',
    __name__,
    url_prefix='/threats'
)