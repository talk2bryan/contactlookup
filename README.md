[![buildstatus](https://github.com/talk2bryan/contactlookup/actions/workflows/ci.yml/badge.svg)](https://github.com/talk2bryan/contactlookup/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/talk2bryan/contactlookup/graph/badge.svg?token=IHS7IJ3RPN)](https://codecov.io/gh/talk2bryan/contactlookup)
[![PyPI version](https://badge.fury.io/py/contactlookup.svg)](https://badge.fury.io/py/contactlookup)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/contactlookup)](https://pypi.org/project/contactlookup/)
[![PyPI - License](https://img.shields.io/pypi/l/contactlookup)](https://pypi.org/project/contactlookup/)
[![PyPI - Format](https://img.shields.io/pypi/format/contactlookup)](https://pypi.org/project/contactlookup/)
[![PyPI - Wheel](https://img.shields.io/pypi/wheel/contactlookup)](https://pypi.org/project/contactlookup/)

# contactlookup
Self hosted contacts API for searching through a VCF file for contact records

## Installation
Using pip:
```bash
pip install contactlookup
```
Using poetry:
```bash
poetry add contactlookup
```
Using pipenv:
```bash
pipenv install contactlookup
```

## Quick Start
As a script:
```bash
contactlookup --help
contactlookup # Start the API server, and serve the contacts in the accompanying contacts.vcf file
contactlookup -f /path/to/contacts.vcf # Start the API server, and serve the contacts in the VCF file
```

As a module:
```bash
python -m contactlookup --help
```

## Examples
### Start and stop the API server
```bash
contactlookup -f /path/to/contacts.vcf # API is now running
```
Kill the server with `Ctrl+C`

### Search for contacts
You can search for contacts by first name, phone number, or email address. The
search is case-insensitive. Partial matches are not yet supported.

#### Search using web browser
Open your web browser and navigate to `http://localhost:8000/docs` to see the API documentation.

#### Search using curl
##### Search by email
```bash
curl -X 'GET' \
  'http://localhost:8000/contacts/email/jeffnewman@example.net' \
  -H 'accept: application/json'
```

##### Search by phone number
```bash
curl -X 'GET' \
  'http://localhost:8000/contacts/phone/+993-547-8840782' \
  -H 'accept: application/json'
```
The use of `+`, `-`, `.`, and `()` in the phone number is optional.
Response:
```json
{
    "contacts": [
        {
            "id": 1,
            "first_name": "KRISTEN",
            "last_name": "PEREZ",
            "other_names": null,
            "company": "Crescendo Associates",
            "title": null,
            "nickname": "NICKNAME",
            "birthday": "1966-08-19",
            "phone_numbers": [
                {
                    "id": null,
                    "number": "7194259182505",
                    "contact_id": 1,
                    "type": null
                },
                {
                    "id": null,
                    "number": "9935478840782",
                    "contact_id": 1,
                    "type": null
                }
            ],
            "addresses": [
                {
                    "id": null,
                    "street": "36346 Hall Stream",
                    "city": "CHRISTOPHERSTAD",
                    "state": "CA",
                    "postal_code": "73297",
                    "contact_id": 1,
                    "type": null,
                    "country": "USA"
                },
                {
                    "id": null,
                    "street": "196 Purple Sage Cres",
                    "city": "WINNIPEG",
                    "state": "MB",
                    "postal_code": "R3X 1V7",
                    "contact_id": 1,
                    "type": null,
                    "country": "CA"
                }
            ],
            "emails": [
                {
                    "id": null,
                    "email": "jacksonkimberly@example.net",
                    "type": null,
                    "contact_id": 1
                }
            ]
        }
    ]
}
```
##### Search by first name
```bash
curl -X 'GET' \
  'http://localhost:8000/contacts/fname/jeff' \
  -H 'accept: application/json'
```
Results are returned in JSON format:
```json
{
    "contacts": [
        {
            "id": 3,
            "first_name": "JEFF",
            "last_name": "",
            "other_names": null,
            "company": "Viagenie",
            "title": null,
            "nickname": null,
            "birthday": "1949-01-29",
            "phone_numbers": [
                {
                    "id": null,
                    "number": "3632144414254",
                    "contact_id": 3,
                    "type": null
                }
            ],
            "addresses": [
                {
                    "id": null,
                    "street": "2360 Bean Tunnel",
                    "city": "SOUTH JAMES",
                    "state": "DC",
                    "postal_code": "96916",
                    "contact_id": 3,
                    "type": null,
                    "country": "MONTSERRAT"
                },
                {
                    "id": null,
                    "street": "26767 Khan Dam",
                    "city": "EAST MARISAMOUTH",
                    "state": "MA",
                    "postal_code": "26701",
                    "contact_id": 3,
                    "type": null,
                    "country": "BRAZIL"
                },
                {
                    "id": null,
                    "street": "63932 Natasha Fords",
                    "city": "DEBRAVIEW",
                    "state": "VT",
                    "postal_code": "22957",
                    "contact_id": 3,
                    "type": null,
                    "country": "NAMIBIA"
                }
            ],
            "emails": [
                {
                    "id": null,
                    "email": "allentaylor@example.net",
                    "type": null,
                    "contact_id": 3
                },
                {
                    "id": null,
                    "email": "daniel03@example.net",
                    "type": null,
                    "contact_id": 3
                },
                {
                    "id": null,
                    "email": "martinezveronica@example.net",
                    "type": null,
                    "contact_id": 3
                }
            ]
        },
        {
            "id": 4,
            "first_name": "JEFF",
            "last_name": "NEWMAN",
            "other_names": null,
            "company": "Hollywood",
            "title": null,
            "nickname": null,
            "birthday": "1955-03-29",
            "phone_numbers": [
                {
                    "id": null,
                    "number": "161555531122",
                    "contact_id": 4,
                    "type": null
                }
            ],
            "addresses": [
                {
                    "id": null,
                    "street": "123 Hollywood St",
                    "city": "BEVERLEY-HILLS",
                    "state": "CA",
                    "postal_code": "22957",
                    "contact_id": 4,
                    "type": null,
                    "country": "USA"
                }
            ],
            "emails": [
                {
                    "id": null,
                    "email": "jeffnewman@example.net",
                    "type": null,
                    "contact_id": 4
                }
            ]
        }
    ]
}
```
