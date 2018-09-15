from marshmallow import fields
from webargs.flaskparser import parser as flaskparser

from backend import db
from backend.helpers.gen_unique_code import generate_unique_code
from backend.helpers.security import SecurityUtils, authorized
from backend.models import *
from backend.schemas import *
from flask import jsonify, request
from flask.views import MethodView

seller_method_view_post_body = {
    'seller': fields.Nested(SellerSchema)
}


class SellerMethodView(MethodView):

    @authorized
    def get(self, seller_id=None):
        if seller_id is not None:
            seller = Seller.query.get_or_404(seller_id)
            catalogs = SellerCatalogs.query.filter_by(seller_id=seller_id)
            # catalog_names = Catalog.query.filter_by()
            return jsonify({
                'sellers': [seller.to_dict()],
                'catalogs': [catalog.to_dict() for catalog in catalogs],
            })

        sellers = SecurityUtils.get_current_seller()  # Seller.query.all()
        return jsonify({
            'sellers': [sellers.to_dict()]
        })

    def post(self):
        dataDict = flaskparser.parse(
            seller_method_view_post_body, request, locations=['json', 'form'])
        print('el dataDICTTTTTTTT', dataDict)
        seller = Seller()
        seller.from_dict(dataDict['seller'])
        user = User.query.get_or_404(seller.user_id)
        seller.code = generate_unique_code(user.first_name, user.id)
        db.session.add(seller)
        db.session.commit()

        return jsonify({'sellers': [seller.to_dict()]})