# JDB

A Simple json based database with context manager support.

## But why ?
While writing my userbot I didnt want to setup a full DB server so I decided to just write my own module.

## Where are the docs ?
They are still a Todo but here's a small example:
```
import jdb
with jdb.Database('test') as db:
    db.set('example', 'value')
    print(db['example'])

````

## Installation
`pip install jdb`
