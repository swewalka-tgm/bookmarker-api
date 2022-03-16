from ast import Return
from operator import ge
from flask import Blueprint,jsonify, request, abort
from validators import url
import validators
from flask_jwt_extended import get_jwt_identity, jwt_required

from src.database import Bookmark,db

bookmarks = Blueprint('bookmarks',__name__,url_prefix='/api/v1/bookmarks')

@bookmarks.route('/', methods = ['POST','GET'])
@jwt_required()
def get_all():
    if request.method == 'POST':
        body = request.json['body']
        url = request.json['url']
        
        if not validators.url(url):
            abort(400,'URL not valid!')
            
        if Bookmark.query.filter_by(url = url).first():
            abort(409,'URL already exists')
            
        bookmark = Bookmark(url=url,body = body, user_id = get_jwt_identity())
        
        db.session.add(bookmark)
        db.session.commit()
        
        return jsonify({
                'id':bookmark.id,
                'url':bookmark.url,
                'short_url':bookmark.short_url,
                'body': bookmark.body,
                'visits':bookmark.visits,
                'created_at':bookmark.created_at,
                'updated_at':bookmark.updated_at
        }),201
        
    else:
        
        page = request.args.get('page',1,type = int)
        per_page = request.args.get('per_page',5,type = int)
        
        all_bookmarks = Bookmark.query.filter_by(user_id = get_jwt_identity()).paginate(page=page,per_page=per_page)
        
        data = []
        
        for bookmark in all_bookmarks.items:
            data.append({
                'id':bookmark.id,
                'url':bookmark.url,
                'short_url':bookmark.short_url,
                'body': bookmark.body,
                'visits':bookmark.visits,
                'created_at':bookmark.created_at,
                'updated_at':bookmark.updated_at
            })
            
        meta = {
            'page':all_bookmarks.page,
            'pages':all_bookmarks.pages,
            'total_count':all_bookmarks.total,
            'prev_page':all_bookmarks.prev_num,
            'next_page':all_bookmarks.next_num,
            'has_next':all_bookmarks.has_next,
            'has_prev':all_bookmarks.has_prev
        }

        return jsonify({'data':data,'meta':meta}),200
    
@bookmarks.get('/<int:id>')
@jwt_required()
def get_bookmark(id):
    
    bookmark = Bookmark.query.filter_by(id=id, user_id= get_jwt_identity()).first()
    
    if bookmark is None:
        abort(404,'bookmark not found')
    
    return jsonify({
            'id':bookmark.id,
            'url':bookmark.url,
            'short_url':bookmark.short_url,
            'body': bookmark.body,
            'visits':bookmark.visits,
            'created_at':bookmark.created_at,
            'updated_at':bookmark.updated_at
    })


@bookmarks.put('/<int:id>')
@bookmarks.patch('/<int:id>')
@jwt_required()
def update_bookmark(id):
    
    body = request.json.get('body','')
    url = request.json.get('url','')
    
    if not validators.url(url):
        abort(401,'URL not valid')
    
    bookmark = Bookmark.query.filter_by(id=id, user_id = get_jwt_identity()).first()
    
    if not bookmark:
        abort(404,'Bookmark not found')
    
    if body:
        bookmark.body = body
        
    if url:
        bookmark.url = url
        
    db.session.commit()
        
    return jsonify({
        'id':bookmark.id,
        'url':bookmark.url,
        'short_url':bookmark.short_url,
        'body': bookmark.body,
        'visits':bookmark.visits,
        'created_at':bookmark.created_at,
        'updated_at':bookmark.updated_at
    }),203
    
@bookmarks.delete('/<int:id>')
@jwt_required()
def delete_bookmark(id):
    
    bookmark = Bookmark.query.filter_by(id=id, user_id = get_jwt_identity()).first()
    
    if not bookmark:
        abort(404,'Bookmark not found')
        
    db.session.delete(bookmark)
    db.session.commit()
    
    return jsonify({
        'message':'bookmark deleted!'
    })
@bookmarks.get('/stats')
@jwt_required()
def get_sats():

    data = []

    bookmarks = Bookmark.query.filter_by(user_id = get_jwt_identity()).all()

    for bookmark in bookmarks:

        new_link = {
            'visits':bookmark.visits,
            'body':bookmark.body,
            'url':bookmark.url
        }
        data.append(new_link)

    return jsonify(data), 200