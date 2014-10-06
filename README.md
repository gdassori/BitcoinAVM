BitcoinAVM
==========

AVM: Awesome(?) (Bitcoin) Vending Machine

Codename: AVM - Awesome(?) Vending Machine, an open source bitcoin ATM based on Django and Electrum.

This project comes up in May 2014, after an Hackaton in march, when I've built a proof-of-concept btc ATM.
Later dlalex83 joined me and we did this. 100% we'll don't finish it, fork and don't let it die.
If forked feel free to contact me to explain or adjust some broken things. mn3monic @ freenode - gdassori @ bitcointalk

Donations: https://greenaddress.it/pay/GALibhqvVEhbZR2NYf6R9DC23L3sq/

Instructions:

- Set up a MySQL Database.
- Set up python2 venv, install dependencies with pip: zbar, django 1.6.6, bitcoinaddress, multiprocessing
- Configure Django settings
- Apply django models on the DB (python manage.py syncdb \ sqlall, check documentation)
- Create a superuser account, (python manage.py createsuperuser)
- Run the app! (python manage.py runserver)
- Login in into admin panel, configure app basics
- Go to the index page (http://127.0.0.1:8000/ ?), since no wallet was created, you should be asked to create a new one. Note your seed and configure the wallet.
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
- Maybe The Rock Trading hasn't the better liquidity of the market, but their customer support rules, and since you rely with customers, you will need a 'txid' ASAP: TRT broadcast the transaction txs on demand, and give back the hash, Bitstamp don't.
(and TRT also have daily spending limits to limit damages if the ATM is stolen). Contact them and ask for a withdrawal API, who knows.
- I now think we did the wrong choice with a SQL database (check the awesomeness of Django + CouchDB in this kind of application).

Hardware:

- Notes reader: NV10 for single way, NV11 with stacker for two-way ATM (they cost about 10keur each, here you can build one for about 1000 euros, is Awesome(VM) ! I also tested it with a Taiko Pub-7, but
I've found it too noisy. Also firmware updates are handled better on NV10. Never tested with NV11, but the two-way trick should be done easily.
- I've tested it on a BeagleBoneBlack + 4DCAPE 70-T 7" touch display from Seeedstudio (they ship in europe in almost a week), is acceptable, but I think you'll need something better for production.
