BitcoinAVM
==========

AVM: Awesome (Bitcoin) Vending Machine

Bitcoin ATM prototype
Codename: AVM - Awesome(?) Vending Machine, an open source bitcoin ATM based on Django and Electrum HD Wallet

This project comes up in April~May 2014, after an Hackaton in march, when I've built a proof-of-concept 24-hours Bitcoin ATM.  Later dlalex83 joined me and we did this. 100% we'll don't finish it, fork and don't let it die.

I'm /r/u/mn3monic - mn3monic @ freenode - gdassori @ bitcointalk 

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
- Credit Card support (Amazon POS ? JUSP ? something else? Easy!)

Advices if forked:

- Our electrum implementation is buggy, feel free to contact me for a GreenAddress wallet wrapper. Using spending limits and 2FA, and a remote script which set them during working time, could enchance
the ATM security: also if it get stolen, no Bitcoins can be taken. 
- Maybe The Rock Trading hasn't the better liquidity of the market, but their customer support ruless, and snce you rely with customers, you need a txid ASAP: TRT broadcast the transaction txs at the moment 
(and also daily have spending limits). Contact them and ask for the withdrawal API.
- I'm on #bitcoin-it @ freenode, contact me there for any need about this project.
- We did the wrong choice with a SQL database (check the awesomeness of Django + CouchDB and get ultrapluriblazed).


Hardware:

- Notes reader: NV10 for single way, NV11 with stacker for two-way ATM (they cost about 10keur each, here you can build one for about 1000 euros, is Awesome(VM) ! I also tested it with a Taiko Pub-7, but
I've found it too noisy. Also firmware updates are handled better on NV10. Never tested with NV11, but the two-way trick should be done easily.
- I've tested it on a BeagleBoneBlack + 4DCAPE 70-T 7" touch display from Seeedstudio (they ship in europe in almost a week), is acceptable, but I think you'll need something better for production.

Donations: https://greenaddress.it/pay/GALibhqvVEhbZR2NYf6R9DC23L3sq/ 
