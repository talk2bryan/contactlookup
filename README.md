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
> [!WARNING]
> The API returns your whole address book to anyone who can reach it. Keep it
> on localhost, or set an API key (see [Configuration](#configuration)) before
> exposing it to your network.

### Running as a Docker container
Serve the contacts in the accompanying sample contacts.vcf file:
```bash
docker build -t contactlookup .
docker run -p 127.0.0.1:8000:8000 contactlookup
# Daemonize the container
docker run -d -p 127.0.0.1:8000:8000 contactlookup
```
To serve your own VCF file, mount it at `/app/contacts.vcf`. Mounting it
read-only is a good idea:
```bash
docker run -d -p 127.0.0.1:8000:8000 \
  -v /path/to/contacts.vcf:/app/contacts.vcf:ro \
  contactlookup
```
To make it reachable from other machines, publish the port on all interfaces
and require an API key:
```bash
docker run -d -p 8000:8000 \
  -e CONTACTLOOKUP_API_KEY="$(openssl rand -hex 32)" \
  -v /path/to/contacts.vcf:/app/contacts.vcf:ro \
  contactlookup
```
The image runs as a non-root user and has a health check on `/health`.

To stop the container:
```bash
docker ps # Get the container ID
docker stop <container_id>
```

### Running as a CLI application
As a script:
```bash
contactlookup --help
contactlookup # Start the API server, and serve the contacts in the accompanying contacts.vcf file
contactlookup -f /path/to/contacts.vcf # Start the API server, and serve the contacts in the VCF file
contactlookup -f /path/to/contacts.vcf --host 0.0.0.0 --port 9000 # listen on all interfaces, port 9000
```
The CLI listens on `127.0.0.1:8000` by default.

### Configuration
| Setting | CLI flag | Environment variable | Default |
|---|---|---|---|
| Address to listen on | `--host` | `CONTACTLOOKUP_HOST` | `127.0.0.1` (`0.0.0.0` in Docker) |
| Port | `--port` | `CONTACTLOOKUP_PORT` | `8000` |
| API key | | `CONTACTLOOKUP_API_KEY` | none (API is open) |

When `CONTACTLOOKUP_API_KEY` is set, every `/contacts` request needs an
`X-API-Key` header:
```bash
curl -H "X-API-Key: $CONTACTLOOKUP_API_KEY" http://localhost:8000/contacts/fname/jeff
```
`/`, `/health` and `/docs` stay open. The key is left out of the CLI flags on
purpose, so it doesn't show up in your shell history or `ps`. If you listen on
anything other than localhost without a key, the app prints a warning at
startup.

### Responses
- `200` with `{"contacts": [...]}` for searches, which is an empty list when
  nothing matches
- `404` for `/contacts/{id}` when there's no contact with that id
- `401` when an API key is configured and the header is missing or wrong
- `503` while the contacts aren't loaded yet

As a module:
```bash
python -m contactlookup --help
```

### Using the API
You can search for contacts by
- first name,
- phone number, or
- email address.

The search is case-insensitive. _Partial matches are not yet supported_.
#### Search using web browser
Open your web browser and navigate to `http://localhost:8000/docs` to see the
API documentation. Depending on your setup, you may need to replace `localhost`.

### Search using curl
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
