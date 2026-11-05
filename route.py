"""Rotas BMVC: transporte HTTP; regras ficam no controlador."""
import os
from pathlib import Path

from bottle import Bottle, redirect, run, static_file
from app.controllers.application import Application
from app.controllers.datarecord import DataRecord

ROOT = Path(__file__).resolve().parent


def create_app(db_path=None):
    app = Bottle()
    ctl = Application(DataRecord(db_path or os.environ.get('BMVC_DB', ROOT / 'app/controllers/db/catalogo.sqlite3'),
                                 os.environ.get('BMVC_USERNAME', 'admin'),
                                 os.environ.get('BMVC_PASSWORD', 'admin123')))
    app.get('/')(lambda: redirect('/portal', code=303))
    app.get('/static/<filepath:path>')(lambda filepath: static_file(filepath, root=str(ROOT / 'app/static')))
    app.get('/portal')(lambda: ctl.render('portal'))
    app.post('/portal')(ctl.login)
    app.post('/logout')(ctl.logout)
    app.get('/banco')(lambda: ctl.render('banco'))
    app.post('/banco')(ctl.write_book)
    app.put('/banco/<book_id:int>')(ctl.write_book)
    app.delete('/banco/<book_id:int>')(ctl.delete_book)
    return app


if __name__ == '__main__':
    run(create_app(), host=os.environ.get('HOST', '0.0.0.0'), port=int(os.environ.get('PORT', '8080')))
