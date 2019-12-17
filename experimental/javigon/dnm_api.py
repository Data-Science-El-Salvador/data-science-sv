import hashlib
import requests
import json
import time
import logging
import sys
import psycopg2 as pg
import string
from datetime import datetime, timezone
import databaseconfig as config
from sqlalchemy import create_engine, MetaData, Table, select
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.engine.url import URL
from sqlalchemy.sql.expression import bindparam
from sqlalchemy.pool import NullPool
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy_utils import get_mapper


engine = create_engine(URL(**config.postgres), poolclass=NullPool, echo=False)
metadata = MetaData()
metadata.reflect(engine)
Base = automap_base(metadata=metadata)
Base.prepare(engine, reflect=True)
Session= sessionmaker(bind=engine, autocommit=True)

_logger = logging.getLogger(__name__)
logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
logging.basicConfig(level=20, stream=sys.stdout,
                    format=logformat, datefmt="%Y-%m-%d %H:%M:%S")

products_api = "http://apiconsulta.medicamentos.gob.sv/public/productos"
def process_products(products, session): 
    products_table = metadata.tables['pharmaceuticals']
    for prod in products:
        timestamp = datetime.utcnow().replace(tzinfo=timezone.utc).replace(microsecond=0).isoformat() 
        hashed = hashlib.md5(json.dumps(prod, sort_keys=True).encode('utf-8')).hexdigest()
        transformed_record  = {"commercial_name": prod['nombreComercial'],
                       "active": prod['Activo'],
                       "inscription_date": prod['FECHA_INSCRIPCION'],
                       "registry_num": prod['noregistro'],
                       "formula": prod['formula'],
                       "active_ingredient": prod['principio_activo'],
                       "pharma_comp": prod['laboratorio'],
                       "pharmaceutical_form": prod['NOMBRE_FORMA_FARMACEUTICA'],
                       "level_price": prod['precio_nivel'],
                       "concentration": prod['concentracion'],
                       "min_presentation_price": prod['precio_presentacion_min'],
                       "max_presentation_price": prod['precio_presentacion_max'],
                       "range_price": prod['precio_rango'],
                       "hash": hashed,
                       "created_at": timestamp,
                       "updated_at": timestamp}
        _logger.info("Record {}".format(transformed_record))
        update_record = session.query(products_table).filter(products_table.c.hash == str(hashed), products_table.c.registry_num != transformed_record['registry_num'])
        if update_record.first() is not None:
            _logger.info(update_record.first())
            del transformed_record['created_at']
            update_record.update(transformed_record)
        else:
            _logger.info("Record {}".format(transformed_record))
            
            session.bulk_insert_mappings((get_mapper(metadata.tables['pharmaceuticals'])), [transformed_record])
                        
def get_products(url):
    session=Session()
    response = requests.get(url) 
    try:  
        response.status_code == 200
        products = response.json()['data']
        process_products(products, session)
        session.close()
        next_url = response.json()['next_page_url']
        next_url = next_url.replace('/?', '?')
    except requests.exceptions.Timeout():
        time.sleep(1)
        get_products(url)
    except.requests.exceptions.RequestException as e:
        _logger.warning(e)
        sys.exit(1)
    _logger.info(next_url)
    return get_products(next_url)
        
        
   
def run():
    get_products(products_api)
    
if __name__ == "__main__":
    run()