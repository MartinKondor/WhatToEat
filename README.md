# WhatToEat

[![Project Status](https://img.shields.io/badge/status-active-brightgreen.svg)](https://w-t-eat.herokuapp.com/)
[![version](https://img.shields.io/badge/version-v1.0.0-brightgreen.svg)](https://github.com/MartinKondor/WhatToEat)
[![GitHub Issues](https://img.shields.io/github/issues/MartinKondor/WildTetris.svg)](https://github.com/MartinKondor/WildTetris/issues)
![Contributions welcome](https://img.shields.io/badge/contributions-welcome-blue.svg)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

Python Flask web server for recommending different recipes with a detailed description, based on what ingredient you would like to eat and what are your preferences.

## Usage

Install dependencies
```shell
$ make install
```

Start the server
```shell
$ python manage.py runserver
```

## Features

- Can search for

    * Lactose free
    * Sugar free
    * Alcohol free
    * Gluten free
    * Vegetarian
    * Vegan
    * Kosher

  kind of foods.
- Up to 100 ingredient can be added
- Free, no ads, no tracking, no cookies

## Structure

```shell
static/
    images/
    scripts/
    stylesheets/
    vendor/  # front end dependencies
templates/
src/
    cook.py  # logic of searching
    utils.py
server.py  # routes
nltk.txt  # nltk dependency
Procfile  # for heroku
```

## License

Copyright (c) 2019 Martin Kondor.
All rights reserved.

See the [LICENSE](LICENSE) file for more details.
