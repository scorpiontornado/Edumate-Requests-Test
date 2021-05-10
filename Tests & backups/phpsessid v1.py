# 25/03/21

'''
URL edumate send you to if you aren't logged in:

https://sacs-login.cloudworkengine.net/module.php/core/loginuserpass.php?AuthState=_23a1e5cd2c788fe4adebd9613b053455d36de30324%3Ahttps%3A%2F%2Fsacs-login.cloudworkengine.net%2Fsaml2%2Fidp%2FSSOService.php%3Fspentityid%3Dhttps%253A%252F%252Fedumate.sacs.nsw.edu.au%252Fsacs%252Fweb%252Fapp.php%26cookieTime%3D1616548941%26RelayState%3D%25257B%252522return_path%252522%25253A%252522dashboard%25255C%25252Fmy-edumate%25255C%25252F%252522%25257D
'''

'''
<div class="login">
    <h3></h3>
	<form action="?" method="post" name="f">

<input type="text" id="username" tabindex="1" name="username" placeholder="Username" value="" autofocus=""><input id="password" type="password" tabindex="2" name="password" placeholder="Password">
            <div class="submit">
<div class="forgot">
<a href="https://sacs-login.cloudworkengine.net/module.php/accountinfo/start-reset.php" target="_blank" class="forgot">I forgot my password</a>
<a href="https://sacs-login.cloudworkengine.net/module.php/accountinfo/forgot-username.php" target="_blank" class="forgot">I forgot my username</a>
</div>
 <input type="submit" onclick="form.submit(); this.disabled=true; this.value='Signing in...';" value="Sign in">
</div>
<input type="hidden" name="AuthState" value="_23a1e5cd2c788fe4adebd9613b053455d36de30324:https://sacs-login.cloudworkengine.net/saml2/idp/SSOService.php?spentityid=https%3A%2F%2Fedumate.sacs.nsw.edu.au%2Fsacs%2Fweb%2Fapp.php&amp;cookieTime=1616548941&amp;RelayState=%257B%2522return_path%2522%253A%2522dashboard%255C%252Fmy-edumate%255C%252F%2522%257D">	</form>
          <p>If you are having trouble logging in, please email itsupport@sacs.nsw.edu.au</p>
</div>
'''

# https://stackoverflow.com/questions/41350762/python-requests-logging-into-website-using-post-and-cookies

import requests

payload = {'username':input("Username: "), 'password':input("Password: ")}
url = 'https://sacs-login.cloudworkengine.net/module.php/core/loginuserpass.php?AuthState=_23a1e5cd2c788fe4adebd9613b053455d36de30324%3Ahttps%3A%2F%2Fsacs-login.cloudworkengine.net%2Fsaml2%2Fidp%2FSSOService.php%3Fspentityid%3Dhttps%253A%252F%252Fedumate.sacs.nsw.edu.au%252Fsacs%252Fweb%252Fapp.php%26cookieTime%3D1616548941%26RelayState%3D%25257B%252522return_path%252522%25253A%252522dashboard%25255C%25252Fmy-edumate%25255C%25252F%252522%25257D'

with requests.Session() as s:
    r = s.post(url, data=payload)
    #cookie = {'PHPSESSID': requests.utils.dict_from_cookiejar(s.cookies)['PHPSESSID']}

    #print(cookie['PHPSESSID'])

    for cookie in requests.utils.dict_from_cookiejar(s.cookies):
      print(cookie)

    print(r, r.text)