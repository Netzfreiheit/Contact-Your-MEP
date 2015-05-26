# pimail - Mail/Faxwidget for the EP


Find a random MEP and write a mail or a fax in your browser.

## Installation

pimail depends on:

* web.py
* Jinja2

install with ```pip install -r requirements.txt```

Edit the mail.tmpl and files in static/ to your liking

Fill data.json with an array of data about the MEPs (or MPs or whatever)

and start with: ``python pimail.py``

this will run a webserver on port 8080

## Contribution

Contributions are always welcome! What you can do

* Test it and give us Feedback (use the github issues)
* Refine the Design - look at the static/ directory and the templates
* Fiddle with the code. Look at the issues and implement missing features.

## embed

you can easily use our widget on your own website. Just copy&paste this html  embed code.

<b>Mail: </b>
`<object data="https://faxjh.savetheinternet.eu/sti/mail/" width="630" height="390" ></object>`

<b>Fax: </b>
`<object data="https://faxjh.savetheinternet.eu/sti/fax/" width="630" height="390" ></object>`

<b>Fax: (only polish S&D MEPs) </b>
`<object data="https://faxjh.savetheinternet.eu/sti/fax/?group=sd&country=pl" width="630" height="390" ></object>`

<b>Fax: (only specific MEP) </b>
`<object data="https://faxjh.savetheinternet.eu/sti/fax/?id=124990" width="630" height="390" ></object>`

<b>Twitter: </b>
`<object data="https://faxjh.savetheinternet.eu/sti/tweet/" width="630" height="390" ></object>`


###How can I translate this tool 
- you make yourself a [github.com](https://github.com) account 
- go to [https://github.com/netzfreiheit/Contact-Your-MEP](https://github.com/netzfreiheit/Contact-Your-MEP)
- click “fork” (you create your own working copy)
- navigate to "static/templates/"
- create a folder with your language short code (e.g. de,en,fr,pl)
- copy the all the files in the "en" folder into this new folder
- translate all english texts into your language
- click “commit changes” 
- click “pull requests”
- click “Click to create a pull request for this comparison” (that's to let us know about your changes to the website)
- you are done and you are great! you helped strg+s the internet <3

**UPDATE:** please always work on up-to-date versions of your forked repository. if you forked your repository some time back then better delete it and fork again (or use comand line to update). 
