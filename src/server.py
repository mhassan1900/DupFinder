#!/usr/bin/env ipython

import tornado.ioloop
import tornado.web

import sys
import os

from tornado.web import RequestHandler

_debug_ = True


class MainHandler(RequestHandler):
    def get(self): # , org, author):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.write('Hello World - go to index page')
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

        print "Setting search mode to < {} >".format(search_mode) #cmpmode or stdmode
        #myname = self.get_query_arguments('fname')     # 'fname': [u'value'] 
        myname = self.get_query_argument('folders2search')   # 'fname': u'value' - raises exception
        print myname
        print 'i got something here', search_mode
        #self.set_header("Content-Type", "application/json")
        search_results = { 'uname': ['abc', 'def'], 'cname': ['XYZ'] }
        self.write( {'search_results': search_results } )


class SearchHandler(RequestHandler):
    def get(self, search_mode): # search/<search_mode>/?<args>
        self.set_header("Access-Control-Allow-Origin", "*")
        folders2search = self.get_query_argument('folders2search')          # gives [u"abc", u"def"]  

        print "Setting search mode to < {} >".format(search_mode) #cmpmode or stdmode
        print 'search mode ->', search_mode
        print 'folders to search->', folders2search

        import numpy as np
        if search_mode == 'stdmode':
            search_results = { 
                'fileA': [np.random.randint(10), 'abc'], 
                'fileB': [np.random.randint(90), 'XYZ'] 
            }
        else: 
            search_results = { 
                'fileA': [np.random.randint(10), 'cmp - abc'], 
                'fileB': [np.random.randint(90), 'cmp - XYZ'] 
            }

        print 'returning', search_results
        self.write( {'search_results': search_results } )



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
        ## (r'/searchmode/([\w]+)', SearchModeHandler),   # need the parenthesis for args in method get()
        (r'/search/([\w]+)', SearchHandler),       # search w/mode info
        ##(r'/search', SearchHandler),                   # search w/o mode info
        (r'/index', MainHandler),  
        (r'/', MainHandler),    #TODO. redirect to frontpage.html
        # anything in static/ directory is now directly accessible from localhost:<port>/ 
        (r'/(.*)', tornado.web.StaticFileHandler, {"path": os.path.join(os.path.dirname(__file__), "static")})
    ], **settings)

    return application



def open_inbrowser(url):
    import webbrowser
    # Open URL in new browser window
    webbrowser.open_new(url) # opens in default browser
    # Opens in safari browser
    webbrowser.get('safari').open_new(url)
    # Open URL in a new tab
    webbrowser.open_new_tab(url) # opens in default browser
    # Opens in safari browser
    webbrowser.get('safari').open_new_tab(url)


def main():
    app = make_app()
    app.listen(8890)
    tornado.ioloop.IOLoop.current().start()

    # attempt to open in new browser window
    # open_inbrowser('localhost:8890/dupfinder.html') 


if __name__ == "__main__":
    main() 
