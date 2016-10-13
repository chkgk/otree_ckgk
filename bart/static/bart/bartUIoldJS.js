function UI (treatment, color, intactSrc, poppedSrc) {

	if (typeof intactSrc === "undefined") {
		intactSrc = "balloon.jpg";
	}
	if (typeof poppedSrc === "undefined") {
		intactSrc = "balloon_popped.jpg";
	}

	this.orangeButtonEnter = function(event) {
		//console.log('mouse enter');
		this.setInstructions('running');
		this.bartController.startAutoPump();
	}

	this.orangeButtonLeave = function(event) {
		if (this.bartController.roundRunning) {
			//console.log('mouse exit');
			this.collectMoney();
			this.show(this.blueButton);
			this.hide(this.orangeButton);
			this.setInstructions('waiting');
			this.updateText(this.blueButton, 'weiter');
			this.waiting = true;
		}
	}

	this.prepare = function() {
		var status = this.bartController.getStatus();
		this.updateText(this.balloonSum, status.currentBalloonSum.toFixed(0));
		this.updateText(this.pumpCount, status.currentStep);
		this.updateText(this.balloonCount, status.balloonCount);
		if (status.exploded) {
			this.setInstructions('boom');
		} else {
			this.setInstructions('standard');
		}
 		
		if (this.treatmentName == 'automatic') {
			this.hide(this.blueButton);
		}

		this.drawBalloon(status.currentSize, status.exploded);
	}

	this.handleExplosion = function(event) {
		if (typeof event.currentSize === 'undefined') {
			return false;
		}
		//console.log('explosion');
		this.hide(this.orangeButton);
		this.show(this.blueButton);
		this.updateText(this.blueButton, "weiter");
		this.updateText(this.balloonSum, "0");
		this.setInstructions('boom');
		this.drawBalloon(event.currentSize, true);
		this.waiting = true;
	}

	this.handleInflation = function(event) {
		if (typeof event.currentSize === 'undefined') {
			return false;
		}
		//console.log('inflation');
		this.drawBalloon(event.currentSize);
		this.updateText(this.balloonSum, event.currentSum.toFixed(0));
		this.updateText(this.pumpCount, event.currentStep);
	}

	this.handleReset = function(event) {
		this.resetEventStorage = event;
		//console.log('reset');
		//console.log(this.resetEventStorage);
	}

	this.handleTaskEnded = function(event) {

		var intactBalloons = [];
		var myPushList = [];

		for (var j = 0; j < event.usedBalloons.length; j++) {
			if (!event.usedBalloons[j].exploded) {
				intactBalloons.push(event.usedBalloons[j]);
			}

			//console.log(event.usedBalloons[j]);
			var timestampArray = event.usedBalloons[j].inflationTimes;
			var deviations = [];
			for (var i = 1; i < timestampArray.length; i++) {
				deviations.push(timestampArray[i]-timestampArray[i-1]);
			}

			var devSum = deviations.reduce(function(pv, cv) { return pv + cv; }, 0);
			
			if (deviations.length > 0) {
				var avgTime = devSum/deviations.length;
				myPushList.push(avgTime);
			}
		}

		var intactPumpAvg = 0;

		if (intactBalloons.length > 0) {
			var intactPumpSum = 0;

			for (var k = 0; k < intactBalloons.length; k++) {
				intactPumpSum += intactBalloons[k].currentStep;
			}
			intactPumpAvg = intactPumpSum / intactBalloons.length;
		}
		

		var data = {
			timestamp: event.timestamp,
			usedBalloons: event.usedBalloons,
			avgPushTimes: myPushList
		};
		
		console.log(event);

		var aTimeSum = myPushList.reduce(function(pv, cv) { return pv + cv; }, 0);

		this.oTreeAvgTime.value = aTimeSum / myPushList.length;
		this.oTreeRawInput.value = JSON.stringify(data);
		this.oTreeTotalCollected.value = event.totalCollected.toFixed(0);

		this.oTreeNumIntact.value = intactBalloons.length;
		this.oTreeAvgPumpsIntact.value = intactPumpAvg;

		this.oTreeForm.submit();
	}

	this.orangeButtonClick = function(event) {
		this.bartController.manualPush();
	}

	this.blueButtonClick = function(event) {
		if (this.treatmentName == 'manual') {
			this.waiting ? this.advanceBalloon() : this.collectMoney();
		} 

		if (this.treatmentName == 'automatic') {
			this.advanceBalloon();
		}
	}

	this.advanceBalloon = function() {
		//console.log('advance');
		this.drawBalloon(this.resetEventStorage.currentSize);
		this.updateText(this.balloonCount, this.resetEventStorage.balloonCount);
		this.show(this.orangeButton);
		if (this.treatmentName == 'automatic') {
			this.hide(this.blueButton);
		}
		this.updateText(this.blueButton, "Punkte sichern");
		this.updateText(this.pumpCount, 0);
		this.updateText(this.balloonSum, "0")
		this.updateText(this.collectedSum, this.resetEventStorage.totalCollected.toFixed(0));
		this.setInstructions('standard');
		this.resetEventStorage = false;
		this.waiting = false
	}

	this.collectMoney = function() {
		//console.log('collectMOney')
		if (this.treatmentName == 'automatic') {
			this.bartController.stopAutoPump();
		}
		this.bartController.collectMoney();
		if(this.treatmentName == 'manual') {
			this.advanceBalloon();
		}
		if(this.treatmentName == 'automatic') {
			this.updateText(this.collectedSum, this.resetEventStorage.totalCollected.toFixed(0));
		}
	}

	this.setInstructions = function(status) {
		var instructions = {
			manual: {
				standard: "<p>Klicken Sie auf \"aufpumpen\" um den Ballon aufzupumpen.</p><p>Klicken Sie auf \"Punkte sichern\" um sich die aktuellen Punkte zu sichern.</p>",
				boom: "<p>Der Ballon ist geplatzt.</p><p>Klicken Sie auf den blauen Button um fortzufahren.</p>",
			},
			automatic: {
				standard: "<p>Ziehen Sie den Mauszeiger auf das rote Feld um mit dem Aufpumpen zu beginnen.</p>",
				waiting: "<p>Punkte gesichert.</p><p>Klicken Sie auf den blauen Button um fortzufahren.</p>",
				running: "<p>Der Ballon wird aufgepumpt.</p><p>Verlassen Sie das rote Feld um die aktuellen Punkte zu sichern.</p>",
				boom: "<p>Der Ballon ist geplatzt.</p><p>Klicken Sie auf den blauen Button um fortzufahren.</p>"
			},
		};
		var selectedInstructions = instructions[this.treatmentName][status];
		this.updateText(this.instructions, selectedInstructions);
	}

	this.updateText = function(element, value) {
		if (typeof element === 'string') {
			element = this.element[element];
		}
		element.innerHTML = value;
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

	this.drawBalloon = function(size, exploded) {
		if (typeof exploded === "undefined") {
			exploded = false;
		}
		var balloonSrc = exploded ? this.imageSrc.exploded : this.imageSrc.intact;
		if (this.balloonImage.src != balloonSrc) {
			this.balloonImage.src = balloonSrc;
		}
		if (this.balloonImage.width != size) {
			this.balloonImage.width = size;
			this.balloonImage.height = size;
		}
	}

	// CONSTRUCTOR
	this.treatmentName = treatment;
	this.balloonColor = color;
	this.treatment = treatment === 'manual' ? 0 : 1;

	this.orangeButton = document.getElementById('balloonPump');
	this.blueButton = document.getElementById('balloonNext');

	this.balloonCount = document.getElementById('balloonCount');
	this.pumpCount = document.getElementById('balloonStep');
	this.balloonSum = document.getElementById('balloonCurrentSum');
	this.collectedSum = document.getElementById('balloonCollectedSum');
	this.instructions = document.getElementById('balloonInstructions');

	this.balloonImage = document.getElementById('balloonImage');

	this.oTreeAvgTime = document.getElementById('id_bart_avg_time');
	this.oTreeRawInput = document.getElementById('id_bart_raw_data');
	this.oTreeTotalCollected = document.getElementById('id_bart_sum_collected');

	this.oTreeNumIntact = document.getElementById('id_bart_num_intact');
	this.oTreeAvgPumpsIntact = document.getElementById('id_bart_avg_pumps_intact');

	this.oTreeForm = document.getElementById('form');

	var self = this;

	this.element = {
		'balloonPump': this.orangeButton,
		'balloonNext': this.blueButton,
		'balloonCount': this.balloonCount,
		'balloonStep': this.pumpCount,
		'balloonCurrentSum': this.balloonSum,
		'balloonCollectedSum': this.collectedSum,
		'balloonInstructions': this.instructions,
		'balloonImage': this.balloonImage,
		'oTreeTotalCollected': this.oTreeTotalCollected,
		'oTreeRawInput': this.oTreeRawInput,
		'oTreeAvgTime': this.oTreeAvgTime,
		'oTreeNumIntact': this.oTreeNumIntact,
		'oTreeAvgPumpsIntact': this.oTreeAvgPumpsIntact
	};

	this.imageSrc = {
		intact: intactSrc,
		exploded: poppedSrc
	}

	this.waiting = false;

	this.orangeButtonDelayIntervalTimer = false;
	this.orangeButtonDelayTime = 250;
	
	this.bartController = new Controller(this.treatment, this.balloonColor);

	this.bartController.addEventListener('inflate', function(e) {
		self.handleInflation(e);
	}, this);

	this.bartController.addEventListener('explode', function(e) {
		self.handleExplosion(e);
	}, this);

	this.bartController.addEventListener('reset', function(e) {
		self.handleReset(e);
	}, this);

	this.bartController.addEventListener('taskEnded', function(e) {
		self.handleTaskEnded(e);
	}, this);

	if (this.treatmentName == 'manual') {
		this.orangeButton.addEventListener('click',	function(e) {
			self.orangeButtonClick(e);
		}, this);
	}
	
	if (this.treatmentName == 'automatic') {
		this.orangeButton.addEventListener('mouseenter', function(e) {
			self.orangeButtonDelayIntervalTimer = setTimeout(function(e) {
				self.orangeButtonEnter(e);
				self.orangeButtonDelayIntervalTimer = false;
			}, self.orangeButtonDelayTime);			
		}, this);

		this.orangeButton.addEventListener('mouseleave', function(e) {
			if (!self.orangeButtonDelayIntervalTimer) {
				self.orangeButtonLeave(e);
			} else {
				clearTimeout(self.orangeButtonDelayIntervalTimer);
				self.orangeButtonDelayIntervalTimer = false;
			}
			
		}, this);	
	}
	

	this.blueButton.addEventListener('click', function(e) {
		self.blueButtonClick(e);
	}, this);

	this.resetEventStorage = false;

	this.prepare();
}
