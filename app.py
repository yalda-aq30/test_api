from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource , Api , reqparse ,fields , marshal_with , abort
from datetime import datetime
from flask_cors import CORS
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
api = Api(app) 
CORS(app)
class ArticleModel(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    title = db.Column(db.String(200), nullable=False)  
    content = db.Column(db.Text, nullable=False)  
    published_date = db.Column(db.DateTime, nullable=False) 
    def __repr__(self):
        return f"Article(title={self.title}, content={self.content[:150]} , published_date={self.published_date} )"  
article_args = reqparse.RequestParser() 
article_args.add_argument("title" , type=str , required=True , help="Title cannot be blanke!" , location='json')
article_args.add_argument("content" , type=str , required=True , help="Content cannot be blanke!" , location='json')
article_args.add_argument('published_date', type=str, required=True, help="Published_data cannot be blank!", location='json')

articleField = {
    "id":fields.Integer,
    "title":fields.String,
    "content":fields.String,
    "published_date":fields.String,
}

class Article(Resource):
    @marshal_with(articleField)
    def get(self):
        article = ArticleModel.query.all() 
        return article 
    @marshal_with(articleField)
    def post(self):
        args = article_args.parse_args()
        if not args["title"] or not args["content"] or not args["published_date"]:
            abort(400, message="Title, Content, and Published Date cannot be blank!")
        published_date = datetime.strptime(args['published_date'], '%Y-%m-%d %H:%M:%S')
        article = ArticleModel(title=args["title"] , content=args["content"] , published_date=published_date)
        db.session.add(article)
        db.session.commit()
        articles = ArticleModel.query.all()
        return articles, 201 

class Articles(Resource):
    @marshal_with(articleField)
    def get(self,id):
        articles = ArticleModel.query.filter_by(id=id).first()
        if not articles:
            abort(404,"Usre not found!")
        return articles
    @marshal_with(articleField)
    def delete(self,id):
        articles = ArticleModel.query.filter_by(id=id).first()
        if not articles:
            abort(404,"Usre not found!") 
        db.session.delete(articles)
        db.session.commit()
        article = ArticleModel.query.all()
        return article
    @marshal_with(articleField) 
    def patch(self,id):
        args = article_args.parse_args()
        articles = ArticleModel.query.filter_by(id=id).first()
        if not articles: 
            abort(404, message="Article not found!") 
        articles.title = args["title"]
        articles.content = args["content"]
        articles.published_date = args["published_date"]
        articles.published_date = datetime.strptime(args["published_date"], "%Y-%m-%d %H:%M:%S") 
        db.session.commit()
        return articles 

        # if args["title"]:
        #     articles.title = args["title"]
        # if args["content"]:
        #     articles.content = args["content"]
        # if args["published_date"]:
            
            # articles.published_date = datetime.strptime(args["published_date"], '%Y-%m-%d %H:%M:%S')


api.add_resource(Article, '/api/articles/')
api.add_resource(Articles, '/api/articles/<int:id>')
@app.route('/')

def home():
    return '<h1> Welcome Yalda </h1>'
if __name__ == "__main__":
    app.run(debug=True)
