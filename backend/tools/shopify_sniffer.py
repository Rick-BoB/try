import shopify
import datetime
import logging
import traceback
import time
import re

# Aggregated Postgresql functions
from sqlalchemy import func

import sys
sys.path.append("../..")
from backend import db
from backend.models import *


SHOPIFY_API_KEY = "02cfc71482e6552378bc7d11e3885bd6"
SHOPIFY_PASSWORD = "e7b9cf6de401f56e47c5d6e2f2c92511"
SHOPIFY_SECRET = "0e22d2e9b9ab59497a2c34e8419caf19"
SHOP_URL = "descubre-belleza.myshopify.com"
SECONDS_TO_FETCH=10


def connect_to_shopify():
    print('Conecting to shopify store...')
    # logger = logging.basicConfig(level=logging.INFO,
    #                              format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    shop_url = "https://{api_key}:{password}@{shopurl}/admin".format(api_key=SHOPIFY_API_KEY,
                                                                     password=SHOPIFY_PASSWORD,
                                                                     shopurl=SHOP_URL)
    shopify.ShopifyResource.set_site(shop_url)


def norm_cellphone(phone):
    return phone.replace(' ', '')


def get_max_id_from_file():
    print('-------------------------------------------------------')
    f = open("max_id.txt", "r")
    max_id = f.read()[:-1]
    f.close()
    # Delete file, afeter the orders iteration will be write again
    print('Get the max_id value stored in file: max_id = {0}'.format(max_id))
    return max_id


def create_new_max_id_file(max_id):
    f = open("max_id.txt", "w")
    f.write(str(max_id) + '\n')
    print('Saving the max_id value in file: max_id = {0}'.format(max_id))
    f.close()


def get_orders_from_shopify():
    max_id = get_max_id_from_file()
    page = 1
    orders_to_enter = []

    while True:
        print('Checking for new orders into shopify store...')
        orders = shopify.Order.find(limit=250, page=page, since_id=max_id)
        if len(orders) > 0:
            orders_to_enter.extend(orders)
            page += 1
        else:
            break

    print('Fetched {0} new orders...'.format(len(orders_to_enter)))
    return orders_to_enter


def save_trouble_order(order_id, message):
    # Read the file:
    f = open("trouble_orders.txt", "r")
    lines = f.readlines()
    f.close()
    f = open("trouble_orders.txt", "w")
    f.write(str(order_id) + "," + message + "\n")
    for line in lines: f.write(line)
    print('Saved into trouble_orders.txt...')
    f.close()


def update_order_table(orders):
    # TODO: Control exceptions and keep the file with max_id
    if len(orders):
        for order in orders:
            order = order.to_dict()
            # Check if phone is empty
            if order['customer']['default_address']['phone'] is None:
                save_trouble_order(order['id'], 'Not phone found into customer-> default_address -> phone')
                create_new_max_id_file(order['id'])
                continue
            # Check if phone contains only numbers
            regex = re.compile("^[0-9]+$")
            phone = norm_cellphone(order['customer']['default_address']['phone'])
            match = regex.match(phone)
            if match is None:
                print('The phone number into order is not a valid number!')
                print('Is not possible to store this order!')
                save_trouble_order(order['id'], 'The phone number into order is not a valid number')
                create_new_max_id_file(order['id'])
                continue
            user_client_id = db.session.query(User.id).filter_by(
                            cellphone=norm_cellphone(order['customer']['default_address']['phone'])).first()

            # Check if user_client_id query returns None, see above ^^
            if user_client_id is not None:
                user_client_id = user_client_id[0]
            # Seller 1 it's the anonymous seller, is used when clients creates order without a seller disccount code
            if len(order['discount_codes']):
                seller_id = db.session.query(Seller.id).filter_by(code=order['discount_codes'][0]['code']).first()[0] if db.session.query(Seller.id).filter_by(code=order['discount_codes'][0]['code']).first() else None
            else:
                seller_id = 1

            print('Processing order {0}...'.format(order['id']))

            if user_client_id is None:
                # Let's create a new one:
                u = User(
                    first_name=order['customer']['first_name'],
                    last_name=order['customer']['last_name'],
                    cellphone=norm_cellphone(order['customer']['default_address']['phone'])
                )
                db.session.add(u)
                try:
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    print('Is not possible to save a new user into database!')
                    print(e)

                c = Client(
                    old_consumer=False, user_id=u.id, profile_id=1, seller_id=seller_id
                )
                db.session.add(c)

                try:
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    print('Is not possible to save a new client into database!')
                    print(e)

                client_id = c.id
            else:
                client_id = db.session.query(Client.id).filter_by(user_id=user_client_id).first()[0] if db.session.query(Client.id).filter_by(user_id=user_client_id).first() else None

            order_ = Order(
                seller_id=seller_id,
                client_id=client_id,
                date=order['updated_at'],
                order_number=order['order_number'],
                total=order['total_price'],
                tax=order['total_tax'],
                shipping=order['shipping_lines'][0]['price']
            )
            db.session.add(order_)

            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print('Is not possible to save a new user into database!')
                print(e)

            create_new_max_id_file(order['id'])
            print('-------------------------- Begin Order --------------------------')
            print('Saving order. ID: {0}, NAME: {1}, TOTAL: {2}, EMAIL: {3}, PHONE: {4}'
                                    .format(order['id'], order['name'], order['total_price'], order['customer']['email'], order['customer']['default_address']['phone']))
            print('-------------------------- End Order --------------------------')
    else:
        print('Nothing to do...')

connect_to_shopify()
while True:
    time.sleep(SECONDS_TO_FETCH)
    orders = get_orders_from_shopify()
    print('Orders List: {0}'.format(orders))
    update_order_table(orders)