from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

# import CRUD Operations from Lesson 1
from database_setup import Base, Restaurant, MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Create session and connect to DB
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


class webServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path.endswith("/restaurants"):
                restaurants = session.query(Restaurant).all()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "</br></br>"
                output += "<a href = '/restaurants/new'> Make a New Restaurant Here </a>"
                for restaurant in restaurants:
                    output += restaurant.name
                    output += "</br>"
                    # Objective 2 -- Add Edit and Delete Links
                    output += "<a href ='/restaurants/%s/edit'>Edit</a>" % restaurant.id
                    output += "</br>"
                    output += "<a href =' #'> Delete </a>"
                    output += "</br></br></br>"
                output += "</body></html>"
                self.wfile.write(output)
                return

            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "Make a New Restaurant </br></br>"
                output += "<form method = 'POST' action = '/restaurants/new' enctype='multipart/form-data'>"
                output += "<input name = 'newRestaurantName' type='text' placeholder='New Restaurant Here'>"
                output += "<input type = 'submit' value ='submit'>"
                # if click 'submit', the form-data will be sent to the action page.
                output += "</html></body>"
                self.wfile.write(output)
                return

            if self.path.endswith("/edit"):
                restaurantID = self.path.split('/')[2]
                restaurantQuery = session.query(Restaurant).filter_by(id=restaurantID).one()
                # Need to check if it's empty, otherwise the name will be updated to empty with a click
                if restaurantQuery != []:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = ""
                    output += "<html><body>"
                    output += "<h1>"
                    output += restaurantQuery.name
                    output += "</h1>"
                    output += "<form method = 'POST' action = '/restaurants/%s/edit' enctype='multipart/form-data'>" % restaurantID
                    output += "<input name = 'updateRestaurantName' type='text' placeholder='%s'>" % restaurantQuery.name
                    output += "<input type = 'submit' value ='Rename'>"
                    # if click 'submit', the form-data will be sent to the action page.
                    output += "</form></body></html>"
                    self.wfile.write(output)
                return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            if self.path.endswith('/restaurants/new'):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messageContent = fields.get('newRestaurantName')
                    newRestaurant = Restaurant(name=messageContent[0])
                    session.add(newRestaurant)
                    session.commit()
                    self.send_response(301)
                    self.send_header('Content-type', 'text-html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()
            if self.path.endswith('/edit'):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messageContent = fields.get('updateRestaurantName')
                    restaurantID = self.path.split('/')[2]
                    restaurantQuery = session.query(Restaurant).filter_by(id=restaurantID).one()
                    if restaurantQuery != []:
                        restaurantQuery.name = messageContent[0]
                        session.add(restaurantQuery)
                        session.commit
                        self.send_response(302)
                        self.send_header('Content-type', 'text-html')
                        self.send_header('Location', '/restaurants')
                        self.end_headers()

        except IOError:
            pass


def main():
    try:
        server = HTTPServer(('', 8080), webServerHandler)
        print 'Web server running...open localhost:8080/restaurants'
        server.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down server'
        server.socket.close()


if __name__ == '__main__':
    main()
