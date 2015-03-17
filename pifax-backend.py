import settings
from html2pdf import HTMLToPDF
import databaseconnect

db = databaseconnect.connect(settings.DATABASE_URL)

def makePDF(line):
	template = tc.get("fax-out.tmpl")
	HTMLToPDF(template.render(line), settings.PDF_uri + '/' + line.id + '.pdf')



# component 1 
# lookup lines to send, parse message into PDF, send out with sendfax command
# db.query("SELECT * FROM faxes WHERE status=0;") 
# 
# sendfax -E -h ttyIAX0@localhost -i "testfax_iax0_acw4_sg" -n -d 004921163558629765 /tmp/testacw4
# sendfax -E -h ttyIAX0@localhost -i "<identifier>" -n -d <destinationnummer> /tmp/<path-to-pdf>


# component 2 logparser 
# /var/spool/hylafax/log/xferfaxlog
# 
# identify all rows for a specific fax, prarse lines and merge this information with the line in the database


# component 3 statistik auswertung 
# produce simple statistic on common errors, warnings and how many attempts a fax usually takes
# calculate the price of each fax and implement a budget maximum 

# component 4 error handling 
# find lines with understood errors and mark those lines in the database for resending

# cronjob to delete fax-message pdfs when exceeding XXX GBs 