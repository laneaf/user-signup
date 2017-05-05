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
import re
import cgi

# html boilerplate for the top of every page
page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>User Signup Form</title>
</head>
<body>
"""
signup_form = """
<h1>Signup</h1>
<form method="post">
<table><tr>
    <td class="label">Username:</td>
    <td><input type="text" name="username" value="%(username)s"/></td>
    <td>
    <label style="color:red;">%(error_username)s</label>
      </td>
    </td>
    </td>
    </tr>
    <tr>
    <td class="label">Password:</td>
    <td><input type="password" name="password" value=""/></td>
    <td>
    <label style="color:red;">%(error_password)s</label>
      </td>
    </tr>
    <tr>
    <td class="label">Verify Password:</td>
    <td><input type="password" name="verify" value=""/></td>
    <td class="error">
    <label style="color:red;">%(error_verify)s</label>
      </td>
    </tr>
    <tr>
    <td class="label">Email(Optional):</td>
    <td><input type="text" name="email" value="%(email)s"/></td>
    <td class="error">
    <label style="color:red;">%(error_email)s</label>
      </td>
    </tr></table>
    <input type="submit" value="Submit"/>
</form>
"""
welcome = """
<h2 style="text-transform: capitalize;">Welcome, {username}!</h2>
</body>
</html>
"""

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return USER_RE.match(username)

PASS_RE = re.compile("^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE = re.compile("^[\S]+@[\S]+.[\S]+$")
def valid_email(email):
    return not email or EMAIL_RE.match(email)

class MainHandler(webapp2.RequestHandler):

    def helper(self, username="",email="", e_username="", e_password="", e_matchpassword="",e_useremail=""):
    #string substitution
        self.response.write(signup_form % { "username": username,
                                "email":email,
                              "error_username": e_username,
                              "error_password": e_password,
                              "error_verify" : e_matchpassword,
                              "error_email": e_useremail})

    def get(self):
        self.helper()

    def post(self):
        have_error = False
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        params = dict(username = username, email = email)

        e_username=""
        e_password=""
        e_matchpassword=""
        e_useremail=""

        if not valid_username(username):
            e_username = "That's not a valid username."
            have_error = True

        if not valid_password(password):
            e_password = "That wasn't a valid password."
            have_error = True
        if password != verify:
            e_matchpassword = "Your password didn't match."
            have_error = True

        if not valid_email(email):
            e_useremail = "Thats not a valid email"
            have_error = True

        if have_error:
            self.helper( username, email, e_username,
                              e_password,
                              e_matchpassword,
                              e_useremail)
            #self.redirect("/?username="+username)
        else:
            self.redirect("/welcome?username="+username)

class Welcome(webapp2.RequestHandler):
   def get(self):
        username = self.request.get('username')
        if valid_username(username):
             self.response.write(welcome.format(username = username))

app = webapp2.WSGIApplication([
('/', MainHandler),
('/welcome', Welcome)
], debug=True)
