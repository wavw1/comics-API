from models import Db
from fastapi import HTTPException

characters = Db(
    characters={
        'spider-man': 620,
        'spider-gwen': 619,
        'batman-comics': 69,
        'batman': 70,
        'bat-girl': 63,
        'ant-man': 30,
        'black-cat': 99,
        'black-panther': 106,
        'bloodhawk': 121,
        'captain-america': 149,
        'captain-marvel': 156,
        'cyclops': 196,
        'daredevil': 201,
        'deadman': 212,
        'deadpool': 213,
        'doctor-doom': 222,
        'doctor-octopus': 225
    }
)

def find_character(character_name: str) -> int:
    try:
        character_id = characters.characters[character_name]
        return character_id
    except:
        raise HTTPException(status_code=400, detail='This character has not found')
    

def all_characters(db: Db):
    characters = []

    for character in db:
        characters.append(character)

    return characters