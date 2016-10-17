function TrafficLightController(treatment) {
	this.construct = function(treatment) {
		CustomEventHandler.apply(this, arguments);
		this.treatment = treatment;
		this.currentColor = '';
		this.isGreen = '';
		this.trialCount = 1;
		this.taskEnded = false;
		this.colors = ['#39f', '#99f', '#f9f', '#fc0'];
		this.colorId = 0;
		
		this.interval = 500;
		this.isRunning = false;
		this.intervalId = false;
	}

	this.start = function() {
		if (this.isRunning) {
			return false;
		}

		this.intervalId = setInterval(function(self) {
			self.changeColor();
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
		
		this.checkColor();
		return true;
	}

	this.manualPush = function() {
		this.changeColor();
	}

	this.changeColor = function(notGreen) {
		if (typeof notGreen === 'undefined') {
			notGreen = false;
		}
		var selectedColor;

		if(notGreen) {
			this.colorId++;
			if (this.colorId > 3) {
				this.colorId = -1;
			}
			this.currentColor = this.colors[this.colorId];
			this.isGreen = false;
		} else {
			this.colorId++;
			if (this.colorId > 3) {
				this.colorId = -1;
				this.isGreen = true;
				this.currentColor = '#0f0';
			} else {
				this.currentColor = this.colors[this.colorId];
				this.isGreen = false;
			}
		}


		var colorChangeEvent = {
			type: 'colorChange',
			color: this.currentColor,
			isGreen: this.isGreen,
			timestamp: Date.now()
		}
		//console.log(this.colorId);
		this.dispatch(colorChangeEvent)
	}

	this.checkColor = function () {
		if (!this.isGreen) {
			// try again
			var trialNotOkEvent = {
				type: 'trialNotOk',
				timestamp: Date.now()
			}
			this.dispatch(trialNotOkEvent);
			//this.reset();
		}
		if (this.isGreen) {
			// okay
			if (this.trialCount < 3) {
				var trialOKEvent = {
					type: 'trialOK',
					trialCount: this.trialCount,
					timestamp: Date.now()
				}
				this.trialCount++;
				this.dispatch(trialOKEvent);
				//this.reset();
			} else {
				this.taskEnded = true;
				var taskEndedEvent = {
					type: 'taskEnded',
					timestamp: Date.now()
				}
				this.dispatch(taskEndedEvent);
			}
		}
	}

	this.reset = function () {
		this.changeColor(true);
		var resetEvent = {
			type: 'reset',
			timestamp: Date.now()
		}
		this.dispatch(resetEvent);
	}

	var self = this;
	this.construct(treatment);
}