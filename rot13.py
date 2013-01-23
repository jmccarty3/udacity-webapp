import webapp2
import cgi

form="""<form method="post">
        <input type=textarea name="text" value="%(data)s"/> 
        <input type="submit"/>
	</form>"""

class Rot13Encoder:
    def __init__(self):
        begin=ord('a')
        end=ord('n')
        self.chipher = {}

        for number in xrange(begin,end):
            key = chr(number)
            value = chr(number+13)
            
            #Keys are transative and I don't know how to do a two way lookup
            self.chipher[key] = value
            self.chipher[value] = key

            key = key.upper()
            value = value.upper()

            self.chipher[key] = value
            self.chipher[value] = key

    def process_data(self, toProcess=""):
        toReturn = ''
        for charecter in toProcess:
            #naive approach
            toReturn+= self.chipher.get(charecter, charecter)

        return cgi.escape(toReturn, quote=True)

class Rot13Page(webapp2.RequestHandler):
    _encoder = None

    def write_form(self, data=""):
	    self.response.write(form % { "data": data} )

    def encoder(self):
        if self._encoder is None:
            self._encoder = Rot13Encoder()
        return self._encoder
    
    def get(self):
      #self.response.headers['Content-Type'] = 'text/plain'
        self.write_form()
    
    def post(self):
        toParse = self.request.get('text')
        finishedData = self.encoder().process_data(toParse)

        print finishedData
        self.write_form(finishedData)

#class RotProcess(webapp2.RequestHandler):
#  def get


app = webapp2.WSGIApplication([('/rot13', Rot13Page)],
                                debug=True)

