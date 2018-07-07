odoo.define('salesdsr.get_geolocation', function(require){
    "use strict";

    var form_widget = require('web.FormController');
    var core = require('web.core');
    var rpc = require('web.rpc');
    var _t = core._t;
    var QWeb = core.qweb;

    form_widget.include({
        _onButtonClicked: function(event) { 
            var self = this;
            if (event.data.attrs.custom === "click"){
                /*var data_id = event.data.record.context.params.id; */
                var data_id = this.getSelectedIds()[0];
                var record_id = event.data.record.data.id;
                if (navigator.geolocation) {
                    navigator.geolocation.getCurrentPosition(showPosition);
                    location.reload();
                } else {
                    alert("Geolocation is not supported by this browser.");
                }
    
                function showPosition(position) {
                    rpc.query({model: 'crm.lead', 
                               method: 'update_location',
                               args: [data_id, position.coords.latitude, position.coords.longitude, record_id]});
                };
                return;
            } 
            else {
                return this._super(event);
            }
        },
    }); 
});
