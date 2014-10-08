BitcoinAVM
==========

AVM: Awesome(?) (Bitcoin) Vending Machine

Codename: AVM - Awesome(?) Vending Machine, an open source bitcoin ATM based on Django and Electrum.



This project comes up in May 2014, after an Hackaton in march, when I've built a proof-of-concept btc ATM.
Later dlalex83 joined me and we did this. 99% we'll don't finish it, fork and don't let it die, or donate and boost us (dont, read below :-) )

*disclaimers:*

*You've the right to blame us for every single line of this code, and probably you would be right.*

*There's no evidence, just speculation, (yet) that a fingerprint reader could be KYC-regulatory-compliant.*

Notes:
======
If forked feel free to contact me to explain or adjust some broken things. mn3monic @ freenode - gdassori @ bitcointalk

General purpose donations: https://greenaddress.it/pay/GALibhqvVEhbZR2NYf6R9DC23L3sq/

Project donations (trackable): 354apm3c8WvU1zBEFBAnv4HNa6Rnf5oUGn - check donation status: http://blockr.io/address/info/354apm3c8WvU1zBEFBAnv4HNa6Rnf5oUGn :


Donations goal (on trackable address, pay attention, and amounts are CUMULATIVE, 2000 eur on the seconds doesn't mean "2000", but 500 of the first +1500 of the second):

- We need ~500 eur for an Innovative Technology NV11 Notes Reader and Banknotes emitter (+beer). If this goal will be achieved, we'll buy it and write a full working, greenaddress based, Two-Ways API for the AVM. Once the funds will be raised, it'll take about 2 weeks to push here the working code.

- We need ~2000 eur for a BeagleBoneBlack (to run android) + mobile POS (and obv +beer) for a cashless AVM. This will be the second achievement, pay attention. Don't send funds for this until the first goal is achieved. Like the first, this second round of funds, if raised, will put us on r&d of the cashless version of the AVM but against this, since no tests are made and we have no idea of how those mobile POS works, we can't give you a deadline. (BTW they have APIs and I don't think it will be a very-very-very hard job).

- Third goal! We need ~3500 eur for a Technodrive Smartclock Bio (+beer) for fingerprint recognition. This will need a lot of beer, the main cost is not about the hardware, but the development of this will surely take more than 100 hours. Really, is not trivial.

- Fourth goal. Oh cmon. We need about ~5000 for a cool case (and when I say cool, I really mean cool). I already have an engineer working on this, and the project ready for prototyping (but since is not my own material, I can't upload them here). This cost is about the prototyping of the hardware, nor me or dlalex will take funds from this (no beer, so). Like the previous, this will not be done till the others 3 are completed. Do not donate for this if you see the previous rounds still need to be reached this readme. This is just a roadmap.

We DON'T encourage donations, but we would really prefeer a fork instead (and we offer free support on what we wrote). Anyway if the amount will be raised, the work will be done as established. 

Probably final costs:

- 300 €: cool case once prototyping
- 200 €: the main hardware (x86 mainboard + atom + ram + etc., or maybe we can switch on Udoo, which looks cool)
- 150 €: the 10" touch display
- 200+50 €: the banknotes reader\emitter and its own PSU (they suck a large amounts of Amperes)
- 200 €: the fingerprint terminal
- 150 €: the POS stuff

So you can have, finally, if the project is finished:

- A two way AVM for about 900 eur
- A two way AVM which can accept payments with credit card for about 1100 eur
- A two way AVM which can accept payments with credit card and do KYC with fingerprint recognition: < 1500 eur

We don't want to waste time on a single way AVM anymore. It doesn't make sense since a lot of cool open source project are out there.

Instructions:

- Set up a MySQL Database.
- Set up python2 venv, install dependencies with pip: zbar, django 1.6.6, bitcoinaddress, multiprocessing
- Configure Django settings
- Apply django models on the DB (python manage.py syncdb \ sqlall, check documentation)
- Create a superuser account, (python manage.py createsuperuser)
- Run the app! (python manage.py runserver)
- Login in into admin panel, configure app basics
- Go to the index page (http://127.0.0.1:8000/ ?), since no wallet was created, you should be asked to create a new one. Note your seed and configure the wallet. Run it with Chromium in Kiosk mode to feel the experience of a real ATM ;-)
- Again, go to next page, the AVM should be ready for Bitcoin selling, fill it if you're brave (I wouldn't, check )

TO DO:

- code revision, exceptions catching, remove debugging code
- better polling on CCTalk
- qrcode & notes reader workers
- angström installation script for AVM clients
- UI for base configuration (internet, intranet credentials, etc.)
- redeem codes for failed transaction
- GSM confirmations & KYC (textanywhere) for buying bitcoins
- auto-exchange @ TheRockTrading, Bitstamp, Kraken, etc. to avoid volatility
- logging module
- database encryption (I would love pycrypto + nosql & encrypt\decrypt data between model and controller)
- code review for better errors handling, logging and warnings
- transactions resume

-------------------
More:

- VAT ?
- implement wallet refill from exchanges
- redeem code generation
- transaction resume (with the redeem code)
- capture email address and send confirmation
- dismiss Electrum and add GreenAddress instant transaction for buying bitcoins with NV11 banknotes reader (two-way cheap CCTalk notes reader, can emit one kind of banknotes * 30)
- credit card support (Amazon POS ? JUSP ? something else?). I wouldn't be afraid of chargebacks, if you take pictures of customers. Its easy and if implemented you get rid of annoying cash management.
- Something like Jumio, and say hi to unfriendly countries

Advices if forked:

- Our electrum implementation is buggy, but feel free to contact me for a GreenAddress wallet wrapper. Using spending limits and 2FA, and a remote script which set them during working time, could enchance the ATM security: also if it get stolen (out of the working time), no Bitcoins can be taken. Seems cool for an ATM.
- We did a very bad practice copying the electrum code and not including the repo, but it's because we had some issues (and no time to fix) with seed recovery between version, and  so we just copied the working version (1.9.6 I guess).
- Maybe The Rock Trading hasn't the better liquidity of the market, but their customer support rules, and since you rely with customers, you will need a 'txid' ASAP: TRT broadcast the txs on demand, and give back the hash, Bitstamp don't.
(and TRT also have daily spending limits to limit damages if the ATM is stolen). Contact them and ask for a withdrawal API, who knows.
- I now think we did the wrong choice with a SQL database (check the awesomeness of Django + CouchDB in this kind of application, maybe you'll need only to change the Django model, and get it working without any other modification).

Hardware:

- Notes reader: NV10 for single way, NV11 with stacker for two-way ATM (they cost about 10keur each, here you can build one for about 1000 euros, is Awesome(VM) ! I also tested it with a Taiko Pub-7, but
I've found it too noisy. Also firmware updates are handled better on NV10. Never tested with NV11, but the two-way trick should be done easily.

- I've tested it on a BeagleBoneBlack + 4DCAPE 70-T 7" touch display from Seeedstudio (they ship in europe in almost a week), is acceptable, but I think you'll need something better for production.

- You really want KYC? You can do easily a fingerprint ID verification with technodrive terminals, they're used in fisical access control systems, made in Italy, I already worked with them, they're cheap and very very strong and powerfull :-) We're talking about a 200eur terminal which handle all the fingerprint part and just gives back the userid, they also have a pinpad, a display, gpio, rs485 and the "TDBASIC" programming language. Take a look to www.technodrive-srl.it, the "smartclock bio" series could be implemented IMHO.
