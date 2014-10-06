window.btcatm = window.btcatm || {};

btcatm.Index = function () {

    this.elements = {
        startBtn: $('#startBtn'),
        welcomeDiv: $('#welcomeDiv'),
        scanAddressDiv: $('#scanAddressDiv'),
        manualAddressBtn: $('#manualAddressBtn'),
        manualAddressTxt: $('#manualAddressTxt'),
        invalidAddressMsg: $('#invalidAddressMsg'),
        paymentDiv: $('#paymentDiv'),
        cancelBtn: $('.cancelBtn'),
        confirmPaymentBtn: $('#confirmPaymentBtn'),
        scanQRBtn: $('#scanQRBtn'),
        qrCodeDiv: $('#qrCodeDiv'),
        csrfToken: $('#csrfmiddlewaretoken'),
        createWalletBtn : $('#createWallet'),
        restoreFromSeedBtn: $('#restoreFromSeedBtn'),
        noWalletDiv: $('#noWalletDiv'),
        walletActionDiv: $('#walletActionDiv'),
        seedDiv: $('#seedDiv'),
        restoreFromSeed: $('#restoreFromSeed'),
        seedForm: $('#seedForm'),
        seedToRestore: $('#seedToRestore'),
        invalidSeedMessage: $('#invalidSeedMessage'),
        insertedCashSpan: $('.insertedCash'),
        btcAmountSpan: $('.btcAmount'),
        destinationAddressSpan: $('.destinationAddress'),
        confirmationDiv: $('#confirmationDiv'),
        startOverBtn: $('#startOverBtn')
    };

    this.qrCodeTimer = 0;
    this.cashMachineTimer = 0;

    this.insertedMoney = 0;
    this.purchasableBTC = 0;
};

btcatm.Index.prototype.init = function () {

    var thisObj = this;

    thisObj.elements.startBtn.on('click', function (e) {
        e.preventDefault();
        thisObj.initTransaction();
    });

    thisObj.elements.manualAddressBtn.on('click', function () {
        var manualAddress = thisObj.elements.manualAddressTxt.val();
        if (manualAddress.length <= 0) {
            thisObj.elements.invalidAddressMsg.fadeIn();
            setTimeout(function () { thisObj.elements.invalidAddressMsg.fadeOut(); }, 5000);
            return;
        }

        btcatm.index.setAddress(manualAddress);


    });

    thisObj.elements.startOverBtn.on('click', function(e){
        e.preventDefault();
        thisObj.reset();
    });

    thisObj.elements.cancelBtn.on('click', function () {
        thisObj.reset();
    });

    thisObj.elements.confirmPaymentBtn.on('click', function () {
        if(thisObj.insertedMoney > 0 && thisObj.purchasableBTC > 0){
            clearInterval(btcatm.index.cashMachineTimer);
            // ajax to confirm purchase
            $.ajax({
                    dataType: 'json',
                    url: '/confirm_payment',
                    type: 'POST',
                    data: {
                        csrfmiddlewaretoken: btcatm.index.elements.csrfToken.val()
                    },
                    success: function (data) {
                        // data should contain tx status
                        btcatm.index.updateInsertedCash(data.notes_inserted, data.btc_amount);
                        btcatm.index.elements.paymentDiv.hide();
                        btcatm.index.elements.confirmationDiv.show();
                        // show confirmation page
                    }
            });
        } else{
            // show message no money instered / no btc available
        }
    });

    thisObj.elements.restoreFromSeed.on('click', function(e){
        e.preventDefault();
        thisObj.elements.walletActionDiv.hide();
        thisObj.elements.seedDiv.show();
    });

    thisObj.elements.restoreFromSeedBtn.on('click', function(e){
        var seed = thisObj.elements.seedToRestore.val();
        if (seed.length <= 0) {
            thisObj.elements.invalidSeedMessage.fadeIn();
            setTimeout(function () { thisObj.elements.invalidSeedMessage.fadeOut(); }, 5000);
            return;
        }
        thisObj.elements.seedForm.submit();
    });

};

btcatm.Index.prototype.initTransaction = function () {

    var thisObj = this;

    $.ajax({
        dataType: 'json',
        url: '/transaction',
        type: 'GET',
        success: function (data) {
            if(data.initialized){
            thisObj.elements.welcomeDiv.hide();
            thisObj.elements.scanAddressDiv.show();
            thisObj.qrCodeTimer = setInterval(thisObj.pollQRReader, 3000);
            } else {
                btcatm.shared.disableAtm();
            }
        },
        error: function(data){
            btcatm.shared.disableAtm();
        }
    });
};

btcatm.Index.prototype.pollQRReader = function () {

    console.log('polling qr code status');
    var thisObj = this;

    $.ajax({
        dataType: 'json',
        url: '/qrcode_status',
        type: 'GET',
        success: function (data) {
            // if address returned
            console.log(data)
            if(data.length > 0){
                clearInterval(btcatm.index.qrCodeTimer);
                // set address
                btcatm.index.setAddress(data);
            }
        }
    });
};

btcatm.Index.prototype.pollCashMachine = function () {
    $.ajax({
        dataType: 'json',
        url: '/notes_status',
        type: 'GET',
        success: function (data) {
            // update money on screen
            // read notes status (data) and display accordingly
            console.log(data);
            if(data != '')
                btcatm.index.updateInsertedCash(data.notes_inserted, data.btc_amount);
        }
    });
};

btcatm.Index.prototype.updateInsertedCash = function(notesInserted, btcAmount){
    btcatm.index.insertedMoney = notesInserted.toFixed(2);
    btcatm.index.purchasableBTC = btcAmount.toFixed(5);
    btcatm.index.elements.btcAmountSpan.html(btcatm.index.purchasableBTC);
    btcatm.index.elements.insertedCashSpan.html(btcatm.index.insertedMoney);
};

btcatm.Index.prototype.reset = function () {
        this.elements.scanAddressDiv.hide();
        this.elements.paymentDiv.hide();
        this.elements.qrCodeDiv.hide();
        this.elements.welcomeDiv.show();
        this.elements.confirmationDiv.hide();
        this.insertedMoney = 0;
        this.purchasableBTC = 0;
        this.elements.btcAmountSpan.html(this.purchasableBTC);
        this.elements.insertedCashSpan.html(this.insertedMoney);
};

btcatm.Index.prototype.setAddress = function(address) {
    $.ajax({
                dataType: 'json',
                url: '/set_address',
                type: 'POST',
                data: {
                    address: address,
                    csrfmiddlewaretoken: btcatm.index.elements.csrfToken.val()
                },
                success: function (data) {
                    // if address returned
                    if(data.success){
                        // address set show insert money page
                         btcatm.index.elements.scanAddressDiv.hide();
                         btcatm.index.elements.destinationAddressSpan.html(address);
                         btcatm.index.elements.paymentDiv.show();
                        if(btcatm.index.qrCodeTimer >= 0)
                            clearInterval(btcatm.index.qrCodeTimer);
                         btcatm.index.cashMachineTimer = setInterval(btcatm.index.pollCashMachine, 5000);
                    } else {
                        console.log('unable to set destination address');
                        btcatm.index.elements.invalidAddressMsg.fadeIn();
                        setTimeout(function () { btcatm.index.elements.invalidAddressMsg.fadeOut(); }, 5000);
                    }
                }
            });
};

btcatm.index = new btcatm.Index();