window.btcatm = window.btcatm || {};

btcatm.Shared = function () {

    this.elements = {
        btcRate: $('#btcRateSpan'),
        csrfToken: $('#csrfToken'),
        contentDiv: $('#contentDiv'),
        atmDisabledDiv: $('#atmDisabledDiv'),
        currencySpan: $('#currencySpan'),
        missingConfigDiv: $('#missingConfigDiv')
    };

    this.btcRateTimer = 0;
    this.enabled = true;
};

btcatm.Shared.prototype.init = function () {

    var thisObj = this;

    thisObj.setRate();
    thisObj.btcRateTimer = setInterval(thisObj.setRate, 10000);
};

btcatm.Shared.prototype.setRate = function () {
    var thisObj = this;

    $.ajax({
        dataType: 'json',
        url: '/machine_status',
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            if(data.error){
                if(data.missing_configuration){
                    clearInterval(btcatm.shared.btcRateTimer);
                }

            } else {
                if(!data.active){
                    btcatm.shared.disableAtm();
                    btcatm.shared.enabled = false;
                } else {
                    if(!btcatm.shared.enabled){
                        btcatm.shared.enableAtm();
                        btcatm.shared.enabled = true;
                    }
                }

                btcatm.shared.elements.btcRate.html(data.exchange_rate);
                btcatm.shared.elements.currencySpan.html(data.currency);
            }
        },
        error: function(data){
            btcatm.shared.disableAtm();
            btcatm.shared.enabled = false;
        }
    });
};

btcatm.Shared.prototype.disableAtm = function () {
        btcatm.shared.elements.atmDisabledDiv.show();
        btcatm.shared.elements.contentDiv.hide();
};

btcatm.Shared.prototype.enableAtm = function () {
        btcatm.shared.elements.atmDisabledDiv.hide();
        btcatm.shared.elements.contentDiv.show();
};


btcatm.shared = new btcatm.Shared();