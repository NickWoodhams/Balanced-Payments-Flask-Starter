from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, validators, TextAreaField, SelectField, SelectMultipleField, HiddenField, RadioField, BooleanField, FileField
from wtforms.validators import ValidationError, Required, Optional
import re

#the astrix means import ALL. for example, this means.. from the package "modules",
#inside the file models, import ALL classes, functions, and variables
#a folder becomes a package when there is an __init__.py file located inside of it.
#without the __init__.py file you cannot import items like your database models
from modules.models import *


#when app.py or another file tries to import items from this file, they will only
#import these items unless explicitly specified, ex. from modules.forms import *
#vs from modules.forms import countries, merchants, demoForm. You can then use these in other files
__all__ = ['demoForm', 'orderDetailsForm']


#create a list of countries for the "countries" select field
#this is a list of tuples. the first value in the tuple is the "value", the second is what is shown to the user
#ex <select name="countries"><option value="US">United States</option></select>
countries = [("", ""), ("AF", "Afghanistan"), ("AX", "Aland Islands"), ("AL", "Albania"), ("DZ", "Algeria"), ("AS", "American Samoa"), ("AD", "Andorra"), ("AO", "Angola"), ("AI", "Anguilla"), ("AQ", "Antarctica"), ("AG", "Antigua and Barbuda"), ("AR", "Argentina"), ("AM", "Armenia"), ("AW", "Aruba"), ("AU", "Australia"), ("AT", "Austria"), ("AZ", "Azerbaijan"), ("BS", "Bahamas, The"), ("BH", "Bahrain"), ("BD", "Bangladesh"), ("BB", "Barbados"), ("BY", "Belarus"), ("BE", "Belgium"), ("BZ", "Belize"), ("BJ", "Benin"), ("BM", "Bermuda"), ("BT", "Bhutan"), ("BO", "Bolivia"), ("BQ", "Bonaire, Saint Eustatius and Saba"), ("BA", "Bosnia and Herzegovina"), ("BW", "Botswana"), ("BV", "Bouvet Island"), ("BR", "Brazil"), ("IO", "British Indian Ocean Territory"), ("BN", "Brunei Darussalam"), ("BG", "Bulgaria"), ("BF", "Burkina Faso"), ("BI", "Burundi"), ("KH", "Cambodia"), ("CM", "Cameroon"), ("CA", "Canada"), ("CV", "Cape Verde"), ("KY", "Cayman Islands"), ("CF", "Central African Republic"), ("TD", "Chad"), ("CL", "Chile"), ("CN", "China"), ("CX", "Christmas Island"), ("CC", "Cocos (Keeling) Islands"), ("CO", "Colombia"), ("KM", "Comoros"), ("CG", "Congo"), ("CD", "Congo, The Democratic Republic Of The"), ("CK", "Cook Islands"), ("CR", "Costa Rica"), ("CI", "Cote D'ivoire"), ("HR", "Croatia"), ("CW", "Curacao"), ("CY", "Cyprus"), ("CZ", "Czech Republic"), ("DK", "Denmark"), ("DJ", "Djibouti"), ("DM", "Dominica"), ("DO", "Dominican Republic"), ("EC", "Ecuador"), ("EG", "Egypt"), ("SV", "El Salvador"), ("GQ", "Equatorial Guinea"), ("ER", "Eritrea"), ("EE", "Estonia"), ("ET", "Ethiopia"), ("FK", "Falkland Islands (Malvinas)"), ("FO", "Faroe Islands"), ("FJ", "Fiji"), ("FI", "Finland"), ("FR", "France"), ("GF", "French Guiana"), ("PF", "French Polynesia"), ("TF", "French Southern Territories"), ("GA", "Gabon"), ("GM", "Gambia, The"), ("GE", "Georgia"), ("DE", "Germany"), ("GH", "Ghana"), ("GI", "Gibraltar"), ("GR", "Greece"), ("GL", "Greenland"), ("GD", "Grenada"), ("GP", "Guadeloupe"), ("GU", "Guam"), ("GT", "Guatemala"), ("GG", "Guernsey"), ("GN", "Guinea"), ("GW", "Guinea-Bissau"), ("GY", "Guyana"), ("HT", "Haiti"), ("HM", "Heard Island and the McDonald Islands"), ("VA", "Holy See"), ("HN", "Honduras"), ("HK", "Hong Kong"), ("HU", "Hungary"), ("IS", "Iceland"), ("IN", "India"), ("ID", "Indonesia"), ("IQ", "Iraq"), ("IE", "Ireland"), ("IM", "Isle Of Man"), ("IL", "Israel"), ("IT", "Italy"), ("JM", "Jamaica"), ("JP", "Japan"), ("JE", "Jersey"), ("JO", "Jordan"), ("KZ", "Kazakhstan"), ("KE", "Kenya"), ("KI", "Kiribati"), ("KR", "Korea, Republic Of"), ("KW", "Kuwait"), ("KG", "Kyrgyzstan"), ("LA", "Lao People's Democratic Republic"), ("LV", "Latvia"), ("LB", "Lebanon"), ("LS", "Lesotho"), ("LR", "Liberia"), ("LY", "Libya"), ("LI", "Liechtenstein"), ("LT", "Lithuania"), ("LU", "Luxembourg"), ("MO", "Macao"), ("MK", "Macedonia, The Former Yugoslav Republic Of"), ("MG", "Madagascar"), ("MW", "Malawi"), ("MY", "Malaysia"), ("MV", "Maldives"), ("ML", "Mali"), ("MT", "Malta"), ("MH", "Marshall Islands"), ("MQ", "Martinique"), ("MR", "Mauritania"), ("MU", "Mauritius"), ("YT", "Mayotte"), ("MX", "Mexico"), ("FM", "Micronesia, Federated States of"), ("MD", "Moldova Republic Of"), ("MC", "Monaco"), ("MN", "Mongolia"), ("ME", "Montenegro"), ("MS", "Montserrat"), ("MA", "Morocco"), ("MZ", "Mozambique"), ("MM", "Myanmar"), ("NA", "Namibia"), ("NR", "Nauru"), ("NP", "Nepal"), ("NL", "Netherlands"), ("AN", "Netherlands Antilles"), ("NC", "New Caledonia"), ("NZ", "New Zealand"), ("NI", "Nicaragua"), ("NE", "Niger"), ("NG", "Nigeria"), ("NU", "Niue"), ("NF", "Norfolk Island"), ("MP", "Northern Mariana Islands"), ("NO", "Norway"), ("OM", "Oman"), ("PK", "Pakistan"), ("PW", "Palau"), ("PS", "Palestinian Territories"), ("PA", "Panama"), ("PG", "Papua New Guinea"), ("PY", "Paraguay"), ("PE", "Peru"), ("PH", "Philippines"), ("PN", "Pitcairn"), ("PL", "Poland"), ("PT", "Portugal"), ("PR", "Puerto Rico"), ("QA", "Qatar"), ("RE", "Reunion"), ("RO", "Romania"), ("RU", "Russian Federation"), ("RW", "Rwanda"), ("BL", "Saint Barthelemy"), ("SH", "Saint Helena"), ("KN", "Saint Kitts and Nevis"), ("LC", "Saint Lucia"), ("MF", "Saint Martin"), ("PM", "Saint Pierre and Miquelon"), ("VC", "Saint Vincent and The Grenadines"), ("WS", "Samoa"), ("SM", "San Marino"), ("ST", "Sao Tome and Principe"), ("SA", "Saudi Arabia"), ("SN", "Senegal"), ("RS", "Serbia"), ("SC", "Seychelles"), ("SL", "Sierra Leone"), ("SG", "Singapore"), ("SX", "Sint Maarten"), ("SK", "Slovakia"), ("SI", "Slovenia"), ("SB", "Solomon Islands"), ("SO", "Somalia"), ("ZA", "South Africa"), ("GS", "South Georgia and the South Sandwich Islands"), ("ES", "Spain"), ("LK", "Sri Lanka"), ("SR", "Suriname"), ("SJ", "Svalbard and Jan Mayen"), ("SZ", "Swaziland"), ("SE", "Sweden"), ("CH", "Switzerland"), ("TW", "Taiwan"), ("TJ", "Tajikistan"), ("TZ", "Tanzania, United Republic Of"), ("TH", "Thailand"), ("TL", "Timor-leste"), ("TG", "Togo"), ("TK", "Tokelau"), ("TO", "Tonga"), ("TT", "Trinidad and Tobago"), ("TN", "Tunisia"), ("TR", "Turkey"), ("TM", "Turkmenistan"), ("TC", "Turks and Caicos Islands"), ("TV", "Tuvalu"), ("UG", "Uganda"), ("UA", "Ukraine"), ("AE", "United Arab Emirates"), ("GB", "United Kingdom"), ("US", "United States"), ("UM", "United States Minor Outlying Islands"), ("UY", "Uruguay"), ("UZ", "Uzbekistan"), ("VU", "Vanuatu"), ("VE", "Venezuela"), ("VN", "Vietnam"), ("VG", "Virgin Islands, British"), ("VI", "Virgin Islands, U.S."), ("WF", "Wallis and Futuna"), ("EH", "Western Sahara"), ("YE", "Yemen"), ("ZM", "Zambia"), ("ZW", "Zimbabwe")]

#create a list of merchants for the "merchants" select field
merchants = [('awesomestuff', 'Awesome stuff, Inc.'), ('stuntmenco', 'Stunt Gear, Inc.'), ('zombiegear', 'Zombie Apocolypse, Inc.')]


#create a WTForms model which makes creating forms very easy
class demoForm(Form):
    merchant = SelectField('Select merchant', [Required()], choices=merchants)
    item = TextField('Item name', [Required()])
    amount = TextField('Amount', [Required()])


class createAccountForm(Form):
    name = TextField('Full name:', [Required()])
    username = TextField('Username', [Required, validators.Length(min=6, max=20), validators.Regexp(r'^[a-zA-Z0-9_]*$')])
    email = TextField('Email:',
                      [validators.Email(),
                      Required()])
    password = PasswordField('Password:',
                             [Required(),
                             validators.Length(min=6, max=120)])

    #this is a custom validator, meaning that every time "validate" method is run on the form it will also run this
    #this is checking to make sure the username is unique in the database otherwise your application will throw an error
    def validate_username(form, field):
        #check to make sure username is unique
        if db_session.query(User).filter_by(username=field.data).count():
            raise ValidationError('Username already exists')


class orderDetailsForm(Form):
    name = TextField('Full name:', [Required()])
    street = TextField(
        'Address Line1',
        [Required(message="Address Line1 is required."), validators.length(max=120)],
        description="Street address, P.O. box, company name, c/o")
    street2 = TextField(
        'Address Line2',
        [Optional(), validators.length(max=120)],
        description="Apartment, suite, unit, building, floor, etc.")
    city = TextField('City', [Required()])
    state = TextField('State', [Required()])
    zip_code = TextField('Zip Code', [Required()])
    country = SelectField('Country', [Required()], choices=countries)
    username = HiddenField(validators=[Required()])
    email = TextField('Email:', [validators.Email(), Required()])
    item = HiddenField(validators=[Required()])
    price = HiddenField(validators=[Required()])
