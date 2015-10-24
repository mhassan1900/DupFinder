import tornado.ioloop
import tornado.web

import sys
import os

from tornado.web import RequestHandler

_debug_ = True


class MainHandler(RequestHandler):
    def get(self): # , org, author):
        self.set_header("Access-Control-Allow-Origin", "*")
        #authors = gs_function.get_related_persons(tc, author)
        #words = gs_function.get_wordfreq_byauth(tc, author)

        self.write('Goodbye World')
        #self.write({
        #    'org': org,
        #    'author': author,
        #    'words': words
        #})

    # -- reference methods --
    #def get(self):
    #    stories = db.stories.find()
    #    self.set_header("Content-Type", "application/json")
    #    self.write(json.dumps(list(stories),default=json_util.default))
  
 
    #def post(self):
    #    story_data = json.loads(self.request.body)
    #    story_id = db.stories.insert(story_data)
    #    print('story created with id ' + str(story_id))
    #    self.set_header("Content-Type", "application/json")
    #    self.set_status(201)


class SearchModeHandler(RequestHandler):
    def get(self, search_mode): # arguments as searchmode/<....>   
        self.set_header("Access-Control-Allow-Origin", "*")
        #myname = self.get_query_arguments('fname')     # 'fname': [u'value'] 
        myname = self.get_query_argument('fname')   # 'fname': u'value' - raises exception
        print myname
        print 'i got something here', search_mode
        #self.set_header("Content-Type", "application/json")
        #self.write('You chose ' + search_mode)
        self.write( {'search_results': search_mode } )


class SearchHandler(RequestHandler):
    def get(self): 
        self.set_header("Access-Control-Allow-Origin", "*")
        print 'Entering search'
        self.write('Will do search now')



#import datetime as dt
#class GetGameByIdHandler(tornado.web.RequestHandler):
#    def get(self, id):
#        response = { 'id': int(id),
#                     'name': 'Crazy Game',
#                     'release_date': dt.date.today().isoformat() }
#        self.write(response)
 




def make_app():
    settings = {
        "template_path": os.path.join(os.path.dirname(__file__), "templates"),
        "static_path": os.path.join(os.path.dirname(__file__), "static"),
        "debug": _debug_ 
    }

    application = tornado.web.Application([
        #(r"/getgamebyid/([0-9]+)", GetGameByIdHandler),
        (r'/searchmode/([\w]+)', SearchModeHandler),   # need the parenthesis for args in method get()
        (r'/search/([\w]+)', SearchModeHandler),
        (r'/search', SearchHandler),
        (r'/index', MainHandler),  
        (r'/', MainHandler),    #TODO. redirect to frontpage.html
        # anything in static/ directory is now directly accessible from localhost:<port>/ 
        (r'/(.*)', tornado.web.StaticFileHandler, {"path": os.path.join(os.path.dirname(__file__), "static")})
    ], **settings)

    return application



def main():
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main() 
