#! env/bin/python

# Name:   migrate.py
# Desc:   Make the updates in db to change the domain of a Wordpress site
# Author: Christopher Perez <christoxl@gmail.com>
# Notes:  This script assumes you have installed MySQL Connector in
#         your environment, you can install it using pip with the
#         command 'pip install mysql-connector'

import mysql.connector

if __name__ == '__main__':
    # Database Information
    db_name = ''
    db_user = ''
    db_password = ''
    db_host = ''  # Change if your database is in another host

    # Set your old and new domain names
    old_domain = ''
    new_domain = ''

    # Make a confguration for the connection
    config = {
        'user': db_user,
        'password': db_password,
        'host': db_host,
        'database': db_name,
        'raise_on_warnings': True,
    }

    # Create the connection to the database
    cnx = mysql.connector.connect(**config)

    # Create a cursor to excute the query
    cursor = cnx.cursor()

    # Updates to execute
    sql_update = """
                UPDATE wp_options
                SET option_value = replace(option_value, '{0}', '{1}')
                WHERE option_name = 'home'
                OR option_name = 'siteurl';

                UPDATE wp_posts
                SET guid = replace(guid, '{0}', '{1}');

                UPDATE wp_posts
                SET post_content = replace(post_content, '{0}', '{1}');

                UPDATE wp_postmeta
                SET meta_value = replace(meta_value, '{0}', '{1}');
                """.format(old_domain, new_domain)

    for result in cursor.execute(sql_update, multi=True):
        print "{} - affected rows = {}".format(result, cursor.rowcount)

    # Make sure data is committed to the database
    cnx.commit()

    # Close the cursor an connection
    cursor.close()
    cnx.close()
