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

header ="<h3>Sign&#45;Up</h3>"
errorcolor = "style = 'color:red'"
class MainHandler(webapp2.RequestHandler):
    def get(self):
        passerror = self.request.get('passerror')
        usernameerror = self.request.get('usernameerror')
        emailerror = self.request.get('emailerror')
        passmiss = self.request.get('passmiss')
        usernameerror_esc = ''
        passerror_esc = ''
        emailerror_esc = ''
        if usernameerror:
            usernameerror_esc = "<span " + errorcolor + ">" + cgi.escape(usernameerror) + "</span>"
        else:
            usernameerror_esc = ''
        if emailerror:
            emailerror_esc = "<span " + errorcolor + ">" + cgi.escape(emailerror) + "</span>"
        if passmiss:
            passerror_esc = "<span " + errorcolor + ">" + cgi.escape(passmiss)+"</span>"
        else:
            if passerror:
                passerror_esc = "<span " + errorcolor + ">"+cgi.escape(passerror)+"</span>"
            else:
                passerror_esc = ''
        username = self.request.get('username')
        email = self.request.get('email')
        if not username:
            username = cgi.escape('')
            if not email:
                email = cgi.escape('')
        userform = """
        <label>
        Username
        <input type = 'text' name='username' value ='{1}' />
        </label>{0}<br>
        """.format(usernameerror_esc,cgi.escape(username))
        passform = """
        <label>
        Password
        <input type ='password' name='password1'/>
        </label>{0}<br>
        <label>
        Verify Password
        <input type ='password' name='password2'/>
        </label>{0}<br>
        """.format(passerror_esc)

        emailform = """
        <label>
        Email
        <input type ='email' name='email' value ='{1}' />
        </label>{0}<br>
        """.format(emailerror_esc,cgi.escape(email))
        form = "<form action ='/signedup' method='post'>"+userform+passform+emailform+"<input type ='submit'/></form>"
        page = header + form
        self.response.write(page)

class SignedUp(webapp2.RequestHandler):
    def post(self):
        username = self.request.get('username')
        pass1 = self.request.get('password1')
        pass2 = self.request.get('password2')
        email = self.request.get('email')
        error = "/?"
        if not username or not pass1 or not pass2 or not email:
            if not username:
                error += "usernameerror=No username given&"
            if not pass1 or not pass2:
                error += "passmiss=No password was given&"
            if not email:
                error += "emailerror=No email given&"
            if '@' not in email or '.' not in email:
                error += "emailerror=Invalid Email address"
        if pass1 and pass2:
            if pass1 != pass2:
                error += "passerror=Passwords don't match&"
        if ' ' in username:
            error += "usernameerror=No spaces allowed&"
        if len(error) > 2:
            if username and email:
                error += "username=" + username + "&email=" + email + "&"
            self.redirect(error)

        body = """
        <h3>Welcome, {0}</h3>
        """.format(username)
        page = header + body
        self.response.write(page)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/signedup', SignedUp)
], debug=True)
