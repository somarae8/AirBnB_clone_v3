#!/usr/bin/python3
"""routes between Places and Amenity """
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request, make_response
from models import storage
from models.place import Place
from models.amenity import Amenity


@app_views.route('/places/<place_id>/amenities',
                 strict_slashes=False, methods=['GET'])
def list_review_place(place_id=None):
    amenities_list = []
    place_obj = storage.get(Place, place_id)

    if place_obj is None:
        abort(404)
    
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        get_amenities = place_obj.amenities
    else:
        get_amenities =  place_obj.amenities_ids
    
    for obj in get_amenities.reviews:
        amenities_list.append(obj.to_dict())
    return jsonify(amenities_list)


@app_views.route('places/<place_id>/amenities/<amenity_id>',
                  strict_slashes=False,
                 methods=['DELETE'])
def del_a_review(place_id=None, amenity_id=None):
    """delete amenity with place_id and"""
    if place_id:
        place_obj = storage.get(Place, place_id)
    
    if amenity_id:
        amenity_obj = storage.get(Amenity, amenity_id)
        
    if place_obj and amenity_id:
    
        if getenv('HBNB_TYPE_STORAGE') == 'db':
            get_amenities = place_obj.amenities
        else:
            get_amenities = place_obj.amenities_ids
        if place_id not in get_amenities:
            abort(404)
        get_amenities.delete(amenity_obj)
        storage.save()
        return (jsonify({})), 200
    else:
        abort(404)


@app_views.route('/places/<string:place_id>/amenities/<string:amenity_id>',
                 methods=['POST'], strict_slashes=False)
def post_place_amenity(place_id, amenity_id):
    """adds an amenity object to a place"""
    get_place = storage.get("Place", place_id)
    get_amenity = storage.get("Amenity", amenity_id)
    if get_place is None or get_amenity is None:
        abort(404)
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        place_amenities = get_place.amenities
    else:
        place_amenities = get_place.amenity_ids
    if get_amenity in place_amenities:
        return jsonify(get_amenity.to_dict())
    place_amenities.append(get_amenity)
    get_place.save()
    return make_response(jsonify(get_amenity.to_dict()), 201)
