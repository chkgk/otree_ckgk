function CustomEventHandler() {
	// Copyright (c) 2010 Nicholas C. Zakas. All rights reserved.
	// MIT License
	// adapted by me.
	this._listeners = {};


    this.addEventListener = function(type, listener, origin) {
        if (typeof this._listeners[type] == "undefined"){
            this._listeners[type] = [];
        }

        this._listeners[type].push([listener, origin]);
    }

    this.dispatch = function(event) {
        if (typeof event == "string"){
            event = { type: event };
        }
        if (!event.target){
            event.target = this;
        }

        if (!event.type){  //falsy
            throw new Error("Event object missing 'type' property.");
        }

        if (this._listeners[event.type] instanceof Array){
            var listeners = this._listeners[event.type];
            for (var i=0, len=listeners.length; i < len; i++){
                listeners[i][0].call(this, event, listeners[i][1]);
            }
        }
    }

    this.removeEventListener = function(type, listener){
        if (this._listeners[type] instanceof Array){
            var listeners = this._listeners[type];
            for (var i=0, len=listeners.length; i < len; i++){
                if (listeners[i][0] === listener){
                    listeners.splice(i, 1);
                    break;
                }
            }
        }
    }
}

if (typeof exports !== 'undefined') {
    if (typeof module !== 'undefined' && module.exports) {
        module.exports.CustomEventHandler = CustomEventHandler;
    }
}