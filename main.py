#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import cgi

header = "<link rel='stylesheet' type='text/css' href='styles.css'><h3>Sign&#45;Up</h3>"

class MainHandler(webapp2.RequestHandler):
    def get(self):
        passerror = self.request.get('passerror')
        if passerror:
            passerror_esc = "<span class = 'error'>"+cgi.escape(passerror)+"</span>"
        else:
            passerror_esc = ''
        userform = """
        <label>
        Username
        <input type = 'text' name='username'/>
        </label><br>
        """
        passform = """
        <label>
        Password
        <input type ='password' name='password1'/>
        </label><br>
        <label>
        Verify Password
        <input type ='password' name='password2'/>
        </label>{0}<br>
        """.format(passerror_esc)

        emailform = """
        <label>
        Email
        <input type ='email' name='email'/>
        </label><br>
        """
        form = "<form action ='/signedup' method='post'>"+userform+passform+emailform+"<input type ='submit'/></form>"
        page = header + form
        self.response.write(page)

class SignedUp(webapp2.RequestHandler):
    def post(self):
        username = self.request.get('username')
        pass1 = self.request.get('password1')
        pass2 = self.request.get('password2')
        email = self.request.get('email')
        if pass1 != pass2:
            self.redirect("/?passerror=Passwords don't match")
        body = """
        username {0} <br>
        pass1 {1} <br>
        pass2 {2} <br>
        email {3} <br>
        """.format(username,pass1,pass2,email)
        page = header + body
        self.response.write(page)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/signedup', SignedUp)
], debug=True)
