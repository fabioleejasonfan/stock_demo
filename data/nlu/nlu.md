## intent:search_stock
<!-- - id, name, type, location, rating… -->
- I want to find [00001](stock_number)
- Give me a type of stock
- I want to find stock in [HK](stock_location)
- Find stock of [Banks](stock_industry)

## intent:stock_detail
<!-- - search, analysis method -->
- Please give me the detail of [00001](stock_number)
- Show me the detail of [00001](stock_number)
- [00001](stock_number)

## intent:stock_opinions
- How does other people think about this stock
- Give me the current news about [00001](stock_number)
- General opotion of [00001](stock_number)

## intent:buy_stock
- I want to buy in [20 hand](hands) [00001](stock_number)

## intent:account_detail
- login
- my account
- setting


## intent:balance_detail
- what stock I have brought

## lookup:stock_location
- HK
- Hong Kong
- USA
- Japan

## lookup:stock_industry
- E-Commerce & Internet Services
- Commercial Vehicle
- Watch & Jewellery
- Banks

## regex:hands
- \d+ hands?

## regex:stock_number
- \d{5}

## intent:affirm
- indeed
- correct
- that sounds good
- yes
- yess please
- of course
- yup
- yeah
- yes please
- yes plz
- Sure
- Ok
- sweet
- cool,
- yes...

## intent:capacity
- What can you do
- What can you answer me
- How do you help me 
- What do you related to
- What is your usage

## intent:deny
- not really
- no
- I don't think so
- never
- no way
- nope
- no thanks
- I dunno
- Nothing!
- nevermind

## intent:goodbye
- see you later
- goodbye
- i'm done
- quit
- stop
- bye
- Adios
- BYEE
- GOODBYE
- Thanks a lot. See ya later

## intent:greet
- good morning
- hi
- hey there
- hey
- good evening
- hello
- Hey RASA!
- Hello?
- Hey Sara!
- HEY
- hello are you still there
- hallo
- HI
- Hey
- Hi
- hi!
- hello there
- hi there
- Hello
- hello its ella

## intent:thankyou
- thank you goodbye
- okay thank you goodbye
- thank you bye
- um okay thank you good bye
- thank you
- and thats all thank you and good bye
- okay thank you
- thanks
- thanks goodbye
- thank you and good bye
- Thanks!

