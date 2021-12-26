import app

_app = app.create_app()
_app.run(host="0.0.0.0", port=3012, debug=True)
