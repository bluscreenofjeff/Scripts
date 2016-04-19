# Scripts

This repo will house any one-off scripts that don't merit their own repo.

## Apache mod_rewrite
Rulesets and supplemental scripts for use with Apache's mod_rewrite to strengthen phishing campaigns. For more info, see my [blog post](https://bluescreenofjeff.com/2016-03-22-strengthen-your-phishing-with-apache-mod_rewrite-and-mobile-user-redirection/) on the subject.
* **Mobile User Redirection** - Redirect any users with mobile device user agents
* **Invalid URI Redirection** - Redirect any requests for non-existant resources
* **Operating System Based Redirection** - Redirect users to different payloads or phishing sites based upon their operating system
* **Combatting Incident Responders** - Use redirection rules to mitigate risks posed by incident responders
* **Phishing Link Expiration** - Expire requests clicked more than a designated number of times. Increases the time it will take incident responders to evaluate the malicious website.

## kali_setup.sh
A script to setup a Kali VM for testing.

## powershell_exe.py
Uses TrustedSec's Powershell Unicorn to generate a powershell payload and wraps it into an EXE using WinRAR under WINE. For setup instructions, see my blog post [Making a Powershell EXE Payload](https://bluescreenofjeff.com/2015-05-13-making-a-powershell-exe-payload/)