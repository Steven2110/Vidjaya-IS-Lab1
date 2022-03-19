from flask import Flask, render_template, request, flash
import json
from WebApp import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
