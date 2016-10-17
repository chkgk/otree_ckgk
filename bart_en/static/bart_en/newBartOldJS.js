function Balloon(id, minSize, maxSize, maxSteps, color) {
	CustomEventHandler.apply(this, arguments);

	this.id = id;
	this.minSize = minSize;
	this.maxSize = maxSize;
	this.maxSteps = maxSteps;
	
	this.color = color;

	this.currentSize = minSize;
	this.currentStep = 0;
	this.exploded = false;

	this.inflationTimes = [];

	this.stepSize = (maxSize-minSize)/maxSteps;

	this.inflate = function () {
		if (this.explodesNow()) {
			this.exploded = true;

			var explodeEvent = {type: 'exploded', timestamp: Date.now(), explodedAt: this.currentStep+1 }
			this.dispatch(explodeEvent);
			return false;
		} 
		this.increaseBalloon();
		return true;

	}


	this.explodesNow = function () {
		// Math.random() proxy for testing
		var r;
		if (typeof module !== 'undefined') {
			var random = require('./randomHelper');
			r = random();
		} else {
			r = Math.random();
		}
		
		return (r <= (1/(this.maxSteps-this.currentStep)));
	}

	this.increaseBalloon = function () {
		this.currentStep++;
		this.currentSize = this.currentSize+this.stepSize;
		this.inflationTimes.push(Date.now());

		var inflateEvent = {timestamp: Date.now(), type: 'inflated', currentStep: this.currentStep, currentSize: this.currentSize };
		this.dispatch(inflateEvent);
	}

	this.reset = function () {
		this.currentSize = this.minSize;
		this.currentStep = 0;
		this.exploded = false;
		var resetEvent = {type: 'reset', timestamp: Date.now() };
		this.dispatch(resetEvent);
	}

	this.isPopped = function () {
		return this.exploded;
	}

	this.snapshot = function() {
		return {
			id: this.id, 
			minSize: this.minSize,
			maxSize: this.maxSize,
			maxSteps: this.maxSteps, 
			stepSize: this.stepSize,
			color: this.color,
			currentStep: this.currentStep,
			currentSize: this.currentSize,
			exploded: this.exploded,
			inflationTimes: this.inflationTimes
		};
	}

	this.toString = function () {
		var state = this.exploded ? "exploded" : "intact";
		var str = "";
		str += "The balloon has a minimum size of "+this.minSize;
		str += " and a maximum size of "+this.maxSize;
		str += ". Its current size is "+this.currentSize;
		str += ", which equals "+this.currentStep;
		str += ". It is "+this.color+" and "+state;
		return str;
	}
}


function Pump() {
	CustomEventHandler.apply(this, arguments);
	this.balloon = false;
	this.pushCount = 0;

	this.push = function () {
		if (!this.balloon) {
			throw new Error("no balloon attached");
		}
		this.pushCount++;
		this.balloon.inflate();
		var pushEvent = {type: 'pushed', pushCount: this.pushCount };
		this.dispatch(pushEvent);
	}

	this.attachNew = function (balloon) {
		this.balloon = balloon;
		this.pushCount = 0;
	}
}

function AutomaticPump(milliSecondsBetweenPushes) {
	if(typeof milliSecondsBetweenPushes !== 'number') {
		throw new Error("missing argument"); 
	}
	Pump.apply(this,arguments);
	this.interval = milliSecondsBetweenPushes;
	this.isRunning = false;
	this.intervalId = false;

	this.start = function() {
		if (this.isRunning) {
			return false;
		}

		this.intervalId = setInterval(function(self) {
			self.push();
		}, this.interval, this);

		this.isRunning = true;
		var startEvent = {type: 'started', timestamp: Date.now() };
		this.dispatch(startEvent);
		return true;
	}

	this.stop = function() {
		if (!this.isRunning) {
			return false;
		}
		clearInterval(this.intervalId);
		this.isRunning = false;
		var stopEvent = {type: 'stopped', timestamp: Date.now() };
		this.dispatch(stopEvent);
		return true;
	}

	this.toggle = function () {
		return this.isRunning ? this.stop() : this.start();
	}

	this.attachNew = function(balloon) {
		if (this.isRunning) {
			throw new Error("cannot attach new balloon while automatic pump is running");
		}
		this.balloon = balloon;
		this.pushCount = 0;
	}

	this.setInterval = function(milliseconds) {
		if (this.isRunning) {
			throw new Error("cannot change interval while automatic pump is running");
		}
		this.interval = milliseconds;
	}
}

function Controller (treatment, color) {

	CustomEventHandler.apply(this,arguments);

	var pushpay = 5;
	if (color == 'green') {
		pushpay = 10;
	}

	this.SETTINGS = {
		MANUAL_TREATMENT: 0,
		AUTO_TREATMENT: 1,
		PUMP_INTERVAL_MS: 250,
		PUSH_PAY: pushpay,
		MAX_TRIALS: 30
	};

	var self = this;

	this.treatment = treatment;
	this.balloonColor = color;

	this.usedBalloons = [];
	this.currentBalloon = false;
	this.totalCollected = 0;
	this.currentBalloonSum = 0;
	this.roundRunning = false;
	this.taskEnded = false;
	

	this.setup = function() {
		if(this.taskEnded) {
			return false;
		}

		if(this.roundRunning) {
			return false;
		}

		var nextBalloon = this.bGeneratorNext();
		if (!nextBalloon) {
			this.endTask();
			return false;
		}

		this.currentBalloon = nextBalloon;

		this.currentBalloon.addEventListener('exploded', this.handleExplosion, this);
		this.currentBalloon.addEventListener('inflated', this.handleInflation, this);

		this.pump.attachNew(this.currentBalloon);

		var uiResetEvent = {
			type: 'reset',
			currentSize: this.currentBalloon.currentSize,
			currentStep: 0,
			currentBalloonSum: 0,
			totalCollected: this.totalCollected,
			balloonCount: this.usedBalloons.length+1
		};
		this.dispatch(uiResetEvent);

		return true;
	}

	this.manualPush = function() {
		if (this.treatment == this.SETTINGS.AUTO_TREATMENT) {
			return false;
		}

		if (!this.roundRunning) {
			this.roundRunning = true;
		}
		
		this.pump.push();
	}

	this.startAutoPump = function() {
		if (this.roundRunning) {
			return false;
		}

		if (this.treatment == this.SETTINGS.MANUAL_TREATMENT) {
			return false;
		}

		this.roundRunning = true;
		this.pump.start();
	}

	this.stopAutoPump = function() {
		if (!this.roundRunning) {
			return false;
		}

		if (this.treatment == this.SETTINGS.MANUAL_TREATMENT) {
			return false;
		}

		this.pump.stop();
		this.roundRunning = false;
	}

	this.handleExplosion = function(event, origin) {
		//console.log('explosion');
		if (typeof origin === 'undefined') {
			var origin = this;
		} 
		if(!origin.roundRunning) {
			return false;
		}
		//console.log(origin);
		if (origin.treatment == origin.SETTINGS.AUTO_TREATMENT) {
			origin.stopAutoPump();
			//console.log('got here');
		}

		origin.roundRunning = false;

		var uiExplodeEvent = {
			type: 'explode', 
			currentSize: origin.currentBalloon.currentSize,
			currentStep: origin.currentBalloon.currentStep,
			currentSum: 0,
			totalCollected: origin.totalCollected
		};
		origin.dispatch(uiExplodeEvent);

		origin.releaseBalloon();
		origin.setup();
	}

	this.handleInflation = function(event, origin) {
		if (typeof origin === 'undefined') {
			var origin = this;
		} 
		origin.currentBalloonSum += origin.SETTINGS.PUSH_PAY
		var uiInflateEvent = {
			type: 'inflate', 
			currentSize: origin.currentBalloon.currentSize,
			currentStep: origin.currentBalloon.currentStep,
			currentSum: origin.currentBalloonSum,
			totalCollected: origin.totalCollected
		};
		origin.dispatch(uiInflateEvent);
	}

	this.handlePush = function(event, origin) {
		origin.currentBalloonSum += origin.SETTINGS.PUSH_PAY;
	}

	this.collectMoney = function() {
		this.roundRunning = false;
		
		if (!this.currentBalloon.isPopped()) {
			this.totalCollected += this.currentBalloonSum;
		}  
		this.releaseBalloon()
		this.setup();
	}

	this.getStatus = function() {
		var statusObject = {
			currentSize: this.currentBalloon.currentSize,
			currentStep: this.currentBalloon.currentStep,
			exploded: this.currentBalloon.isPopped(),
			currentBalloonSum: this.currentBalloonSum,
			totalCollected: this.totalCollected,
			balloonCount: this.usedBalloons.length+1
		};
		return statusObject;
	}

	this.endTask = function () {
		this.taskEnded = true;
		var uiTaskEndedEvent = {
			type: 'taskEnded',
			timestamp: Date.now(),
			usedBalloons: this.usedBalloons,
			totalCollected: this.totalCollected
		};
		this.dispatch(uiTaskEndedEvent);
	}

	this.releaseBalloon = function () {
		this.storeSnapshot();
		this.currentBalloon.removeEventListener('exploded', this.handleExplosion);
		this.currentBalloon.removeEventListener('inflated', this.handleInflation);
		this.currentBalloonSum = 0.0;
	} 

	this.storeSnapshot = function() {
		if(this.roundRunning) {
			return false;
		}

		self.usedBalloons.push(self.currentBalloon.snapshot());
	}

	this.determinePump = function() {
		if (this.treatment == this.SETTINGS.MANUAL_TREATMENT) {
			return new Pump();
		}

		if (this.treatment == this.SETTINGS.AUTO_TREATMENT) {
			return new AutomaticPump(this.SETTINGS.PUMP_INTERVAL_MS);
		}
	}

	this.prepareBalloonList = function(color) {
		// could read from file etc.
		// var balloonList = [
		// 		{ 
		// 			id: 1,
		// 			minSize: 100,
		// 			maxSize: 600,
		// 			maxSteps: 128
		// 		},
		// 		{ 
		// 			id: 2,
		// 			minSize: 100,
		// 			maxSize: 600,
		// 			maxSteps: 128
		// 		},
		// 		{ 
		// 			id: 3,
		// 			minSize: 100,
		// 			maxSize: 600,
		// 			maxSteps: 128
		// 		}
		// 	];

		var maxSteps = 128;

		if (color == "green") {
			maxSteps = 64;
		} 

		var balloonList = [];

		for (var i = 0; i < this.SETTINGS.MAX_TRIALS; i++) {
			balloonList.push({
				id: i,
				minSize: 100,
				maxSize: 600,
				maxSteps: maxSteps,
				color: color
			});
			
		}
		return balloonList;
	}


	this.bGeneratorNext = function() {
		if (this.bIndex >= this.balloonList.length) {
			return false;
		}
		var balloon = new Balloon(
					this.balloonList[this.bIndex].id,
					this.balloonList[this.bIndex].minSize,
					this.balloonList[this.bIndex].maxSize,
					this.balloonList[this.bIndex].maxSteps,
					this.balloonList[this.bIndex].color
				);
		this.bIndex++;
		return balloon;
	}
	this.bIndex = 0;

	this.pump = this.determinePump();
	this.balloonList = this.prepareBalloonList(this.balloonColor);

	this.setup();
}

if (typeof exports !== 'undefined') {
	if (typeof module !== 'undefined' && module.exports) {
		module.exports.Balloon = Balloon;
		module.exports.Pump = Pump;
		module.exports.AutomaticPump = AutomaticPump;
		module.exports.Controller = Controller; 
	}
}