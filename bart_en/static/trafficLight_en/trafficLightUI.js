function TrafficLightUI(treatment) {
	this.construct = function(treatment) {
		this.treatmentName = treatment;
		this.orangeButton = document.getElementById('lightSwitch');
		this.blueButton = document.getElementById('balloonNext');
		this.light = document.getElementById('light');
		this.infoBox = document.getElementById('trafficLightInfo');
		this.mouseOver = false;
		this.taskEnded = false;

		this.element = {
			'lightSwitch': this.orangeButton,
			'balloonNext': this.blueButton,
			'trafficLightInfo': this.infoBox,
			'light': this.light
		}

		this.Controller = new TrafficLightController(treatment);

		this.Controller.addEventListener('colorChange', function(e) {
			self.switchLightColor(e.color);
		});

		this.Controller.addEventListener('reset', function (e) {
			//console.log('reset');
		});

		this.Controller.addEventListener('trialNotOk', function(e) {
			var text;
			if (treatment == 'manual') {
				text = "<p>That was not correct. Please try again.</p>\
				<p>Repeatedly click on the red button until the circle turns green. Then, click 'next'.</p>";
			} else {
				text = "<p>That was not correct. Move the cursor onto the red field.</p>\
				<p>As soon as the circle turns green, pull the cursor off the field.</p>";
			}
			
			self.setInfoText(text);
		});

		this.Controller.addEventListener('trialOK', function(e) {
			//console.log('trial ok');
			var text = "<p>Very good! Try it again (trial "+e.trialCount+" of 3)!</p>";
			self.setInfoText(text);
		});

		this.Controller.addEventListener('taskEnded', function(e) {
			//console.log('task ended');
			var text = "<p>Very good! You have done it correctly for three times.</p>\
			<p>Click 'next' to move on.</p>";
			self.taskEnded = true;
			self.hide(self.orangeButton);
			self.setInfoText(text);
		});

		if (this.treatmentName == 'manual') {
			this.orangeButton.addEventListener('click',	function(e) {
				self.orangeButtonClick(e);
			}, this);
			this.setInfoText("<p>Repeatedly click on the red button until the circle turns green. Then, click 'next'.</p>");
		}
		
		if (this.treatmentName == 'automatic') {
			this.orangeButton.addEventListener('mouseenter', function(e) {
				self.orangeButtonEnter(e);
			}, this);

			this.orangeButton.addEventListener('mouseleave', function(e) {
				self.orangeButtonLeave(e);
			}, this);
			this.setInfoText("<p>Move the cursor onto the red field.</p><p>As soon as the circle turns green, pull the cursor off the field.</p>");
			this.hide(this.blueButton);
		}

		this.blueButton.addEventListener('click', function(e) {
			self.blueButtonClick(e);
		}, this);

		this.Controller.changeColor(true);
	}

	this.hide = function(element) {
		if (typeof element === 'string') {
			element = this.element[element];
		}
		element.style.display = 'none';
	}

	this.show = function(element) {
		if (typeof element === 'string') {
			element = this.element[element];
		}
		element.style.display = 'block';
	}

	this.switchLightColor = function(color) {
		this.light.style.backgroundColor = color;
	}

	this.setLightText = function(text) {
		this.light.innerHTML = text;
	}

	this.setInfoText = function(text) {
		this.infoBox.innerHTML = text;
	}

	this.orangeButtonClick = function (event) {
		//console.log("orangeButtonClick");
		this.Controller.manualPush();
		// pump once
	}

	this.orangeButtonEnter = function (event) {
		//console.log("orangeButtonEnter");
		this.mouseOver = true;
		setTimeout(function(event, obj) {
			if (obj.mouseOver) {
				//console.log('executing code');
				obj.Controller.start();
			}
		}, 200, event, this);
	}

	this.orangeButtonLeave = function(event) {
		this.mouseOver = false;
		//console.log("orangeButtonLeave");
		this.Controller.stop()
		this.hide(this.orangeButton);
		this.show(this.blueButton);
	}

	this.blueButtonClick = function(event) {
		//console.log("blueButtonClick");
		// next trial
		// or finish trial session
		if (!this.taskEnded) {
			if (this.treatmentName == 'automatic') {
				this.show(this.orangeButton);
				this.hide(this.blueButton);
			}

			if (this.treatmentName == 'manual') {
				this.Controller.checkColor();
				this.Controller.reset();
			}
		} else {
			// taskEnded == true
			this.submitForm();
		}
	} 

	this.submitForm = function() {
		// handle oTree stuff.
		//console.log('form submit, moving on');
		this.oTreeForm = document.getElementById('form');
		this.oTreeForm.submit();

	}

	var self = this;
	this.construct(treatment);
}