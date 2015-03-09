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
`<object data="https://faxjh.savetheinternet.eu/" width="630" height="390" ></object>`

<b>Fax: </b>
`<object data="https://faxjh.savetheinternet.eu/fax/" width="630" height="390" ></object>`

<b>Fax: (only polish S&D MEPs) </b>
`<object data="https://faxjh.savetheinternet.eu/fax/?group=sd&country=pl" width="630" height="390" ></object>`

<b>Fax: (only specific MEP) </b>
`<object data="https://faxjh.savetheinternet.eu/fax/?id=124990" width="630" height="390" ></object>`

<b>Twitter: </b>
`<object data="https://faxjh.savetheinternet.eu/tweet/" width="630" height="390" ></object>`
