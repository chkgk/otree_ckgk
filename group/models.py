from otree.api import (
	models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
	Currency as c, currency_range
)

import random

author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
	name_in_url = 'group'
	players_per_group = None
	num_rounds = 1

	category_names = ['sehr konservativ', 'sicherheitsorientiert', 'ausgeglichen', 'wachstumsorientiert', 'offensiv']

	duration = 45

	endowment_principals = c(10)

	# Fixed Compensation
	fixed_payment = c(5)

	#Variable Compensation
	variable_payment = c(5)			# Fixer Anteil für die Agenten
	share_result = 25
	share_profit = 35


class Subsession(BaseSubsession):

	def creating_session(self):
		random_number = random.randint(1,2)
		player_list = self.get_players()
		for player in player_list:
			player.compensation = self.session.config["compensation"]
			player.participation_fee = self.session.config["participation_fee"]
			player.random_number = random_number
	
	def set_groups(self):

		# Create category lists

		cat_lists = dict.fromkeys(Constants.category_names)
		for element in cat_lists:
			cat_lists[element] = []

		# sort players into category lists by their choices
		for player in self.get_players():
			for cat_name in cat_lists:
				if player.category == cat_name:
					cat_lists[cat_name].append(player)
					

		total_players = len(self.get_players())
		group_size = 6
		number_groups = int(total_players / group_size)

		print(cat_lists)

		groups = [[] for i in range(number_groups)]
		temp = []
		for i in range(len(Constants.category_names)):
			for j in range(len(cat_lists[Constants.category_names[i]])):
				temp.append(cat_lists[Constants.category_names[i]][j])
		
		print(temp)
		for i in range(number_groups):
			print(temp[i::number_groups])
			groups[i].append(temp[i::number_groups])

		print([l[0] for l in groups])
		matrix = [l[0] for l in groups]

		# matrix = [[2, 1], [4,3]]


		self.set_group_matrix(matrix)

		print(self.get_group_matrix())

		group_matrix = self.get_group_matrix()
		for group in group_matrix:
			for player in group:
				player.my_group_id = group_matrix.index(group) + 1


	def communicate_categories(self):
		for group in self.get_groups():
			for player in group.get_players():
				player.find_principals()
				player.find_partners()
				player.get_category()


class Group(BaseGroup):
	
	def after_investments(self):
		#self.investment_success = (random.random() <= 1/3)
		for player in self.get_players():
			player.get_investment()
			player.calculate_payoffs_principals()
			player.get_outcome_of_principal()


	def after_results_principals(self):
		for player in self.get_players():
			player.get_invested_amount()
			player.get_msg_payoff_profit()
			player.calculate_payoffs_agents()


class Player(BasePlayer):

	my_group_id = models.IntegerField()

	random_number = models.IntegerField()

	compensation = models.CharField(
		doc="Compensation scheme put in place for agents (see Settings)."
		)

	participation_fee = models.CurrencyField(
		doc="Participation fee for all agents."
		)



	# Gerade Nummern sind Prinzipale und ungerade Agenten
	def role(self):
		return "Principal" if self.id_in_group % 2 == 0 else "Agent"


# Assign partners (i.e. build principal agent couples: 1-2, 3-4, 5-6)

	partner = models.IntegerField(
		doc="Gives the ID in Group of the partner.")

	def find_partners(self):
		if self.id_in_group == 1:
			self.partner = 2
		elif self.id_in_group == 2:
			self.partner = 1
		elif self.id_in_group == 3:
			self.partner = 4
		elif self.id_in_group == 4:
			self.partner = 3
		elif self.id_in_group == 5:
			self.partner = 6
		elif self.id_in_group == 6:
			self.partner = 5



# Everyone chooses the category:

	category = models.CharField(
		choices=Constants.category_names,
		widget=widgets.RadioSelect(),
		verbose_name="Bitte wählen Sie nun einen der fünf Begriffe:",
		doc="Principals choose the category which is communicated to their agent"
		)


	category_from_principal = models.CharField(
		doc="Category that agents receive from their principals indicating how they want their agent to invest. Only for the agent who is payoff relevant."
		)


	def get_category(self):
		if self.role() == "Agent":
			principal = self.get_others_in_group()[int(self.partner)-2]
			self.category_from_principal = principal.category



# Part II: Investment for Group members
	
	c_principal_1 = models.CharField()
	c_principal_2 = models.CharField()
	c_principal_3 = models.CharField()
	c_principal_4 = models.CharField()
	c_principal_5 = models.CharField()

	def find_principals(self):

		# c for corresponding
		if self.id_in_group == 1:
			self.c_principal_1 = 2
			self.c_principal_2 = 3
			self.c_principal_3 = 4
			self.c_principal_4 = 5
			self.c_principal_5 = 6
		elif self.id_in_group == 2:
			self.c_principal_1 = 1
			self.c_principal_2 = 3
			self.c_principal_3 = 4
			self.c_principal_4 = 5
			self.c_principal_5 = 6
		elif self.id_in_group == 3:
			self.c_principal_1 = 1
			self.c_principal_2 = 2
			self.c_principal_3 = 4
			self.c_principal_4 = 5
			self.c_principal_5 = 6
		elif self.id_in_group == 4:
			self.c_principal_1 = 1
			self.c_principal_2 = 2
			self.c_principal_3 = 3
			self.c_principal_4 = 5
			self.c_principal_5 = 6
		elif self.id_in_group == 5:
			self.c_principal_1 = 1
			self.c_principal_2 = 2
			self.c_principal_3 = 3
			self.c_principal_4 = 4
			self.c_principal_5 = 6
		elif self.id_in_group == 6:
			self.c_principal_1 = 1
			self.c_principal_2 = 2
			self.c_principal_3 = 3
			self.c_principal_4 = 4
			self.c_principal_5 = 5


	decision_for_p1 = models.CurrencyField(
		min=0,
		max=Constants.endowment_principals,
		widget=widgets.Slider(),					# Neuer Slider von Christian
		verbose_name="Ihre Investitionsentscheidung für Ihren Kunden:",
		doc="Agents investment for the principal in the risky asset."
		)
		
	decision_for_p2 = models.CurrencyField(
		min=0,
		max=Constants.endowment_principals,
		widget=widgets.Slider(),					# Neuer Slider von Christian
		verbose_name="Ihre Investitionsentscheidung für Ihren Kunden:",
		doc="Agents investment for the principal in the risky asset."
		)

	decision_for_p3 = models.CurrencyField(
		min=0,
		max=Constants.endowment_principals,
		widget=widgets.Slider(),					# Neuer Slider von Christian
		verbose_name="Ihre Investitionsentscheidung für Ihren Kunden:",
		doc="Agents investment for the principal in the risky asset."
		)

	decision_for_p4 = models.CurrencyField(
		min=0,
		max=Constants.endowment_principals,
		widget=widgets.Slider(),					# Neuer Slider von Christian
		verbose_name="Ihre Investitionsentscheidung für Ihren Kunden:",
		doc="Agents investment for the principal in the risky asset."
		)

	decision_for_p5 = models.CurrencyField(
		min=0,
		max=Constants.endowment_principals,
		widget=widgets.Slider(),					# Neuer Slider von Christian
		verbose_name="Ihre Investitionsentscheidung für Ihren Kunden:",
		doc="Agents investment for the principal in the risky asset."
		)



# principals can send messages to their agents:

	message = models.CharField(
		choices=["Ich bin sehr zufrieden mit Ihrer Entscheidung", "Ich bin zufrieden mit Ihrer Entscheidung",
		"Ich bin unzufrieden mit Ihrer Entscheidung", "Ich bin sehr unzufrieden mit Ihrer Entscheidung"],
		widget=widgets.RadioSelect(),
		verbose_name="Wählen Sie dazu eine der vorgefertigten Mitteilungen aus:",
		doc="Principals choose the message to send to the agents."
		)


	message_from_principal = models.CharField(
		doc="Message that agents receive from their principals."
		)


# Payoffs:

	investment = models.CurrencyField(
		doc="Indicates for everyone the investment decision as taken by their agents."
		)

	def get_investment(self):
		if self.role() == "Principal":
			agent = self.get_others_in_group()[int(self.partner)-1]
			if self.id_in_group == 2:
				self.investment = agent.decision_for_p1
			if self.id_in_group == 4:
				self.investment = agent.decision_for_p3
			if self.id_in_group == 6:
				self.investment = agent.decision_for_p5


	# Damit die Agenten ihre Investitionen für den für die Auszahlung relevanten Prinzipal sehen:

	invested_amount = models.CurrencyField(
		doc="For agents, this gives us the investment in the risky option for their relevant principal (agents own decision).")

	def get_invested_amount(self):
		if self.role() == "Agent":
			principal = self.get_others_in_group()[int(self.partner)-2]
			self.invested_amount = principal.investment




	# Investition in risky asset: Erfolgreich oder nicht erfolgreich:
	def determine_outcome(self):
		randomizer = random.randint(1,3)
		if self.role() == "Principal":
			if randomizer == 1:
				self.investment_outcome = 1
			else:
				self.investment_outcome = 0

	investment_outcome = models.IntegerField(
		doc="Turns 1 if the investment was successful and 0 in case it was not."
		)


	# Get outcome of the principals as a variable for the agents:

	outcome_of_principal = models.IntegerField(
		doc="Message that agents receive from their principals."
		)

	def get_outcome_of_principal(self):
		if self.role() == "Agent":
			principal = self.get_others_in_group()[int(self.partner)-2]
			self.outcome_of_principal = principal.investment_outcome



	def calculate_payoffs_principals(self):
		if self.role() == "Principal":
			if self.investment_outcome == 1:
				self.payoff = self.investment * 3.5 + (Constants.endowment_principals - self.investment)
				self.profit = self.investment * 2.5
			elif self.investment_outcome == 0:
				self.payoff = Constants.endowment_principals - self.investment
				self.profit = 0


	profit = models.CurrencyField(
		doc="Gives the profit of the principal."
		)

	payoff_of_principal = models.CurrencyField(
		doc="Gives for each agent the payoff of his principal."
		)

	profit_of_principal = models.CurrencyField(
		doc="Gives for each agent the payoff of his principal."
		)


	def get_msg_payoff_profit(self):
		if self.role() == "Agent":
			principal = self.get_others_in_group()[int(self.partner)-2]
			self.profit_of_principal = principal.profit
			self.payoff_of_principal = principal.payoff
			self.message_from_principal = principal.message


	def calculate_payoffs_agents(self):
		if self.role() == "Agent":
			if self.compensation == "fixed":
				self.payoff = Constants.fixed_payment
			if self.compensation == "variable_result":
				self.payoff = Constants.variable_payment + Constants.share_result/100 * self.payoff_of_principal
			if self.compensation == "variable_profit":
				self.payoff = Constants.variable_payment + Constants.share_profit/100 * self.profit_of_principal



	# Comprehension Questions
	question_1 = models.CharField(
		widget=widgets.RadioSelectHorizontal(),
		choices=["Richtig", "Falsch"])

	question_2 = models.CharField(
		widget=widgets.RadioSelectHorizontal(),
		choices=["Richtig", "Falsch"])

	question_3 = models.CurrencyField()

	question_4 = models.CurrencyField()

	question_5 = models.CharField(
		widget=widgets.RadioSelectHorizontal(),
		choices=["Richtig", "Falsch"])

	question_6 = models.CharField(widget=widgets.RadioSelectHorizontal(), choices=["Richtig", "Falsch"])





	# Questionnaire:
	age = models.PositiveIntegerField(
		max=100,
		verbose_name="Wie alt sind Sie?",
		doc="We ask participants for their age between 0 and 100 years"
		)

	gender = models.CharField(
		choices=["männlich", "weiblich", "anderes"],
		widget=widgets.RadioSelect(),
		verbose_name="Was ist Ihr Geschlecht?",
		doc="gender indication"
		)

	studies = models.CharField(
		blank=True,
		verbose_name="Was studieren Sie im Hauptfach?",
		doc="field of studies indication."
		)

	nonstudent = models.BooleanField(
		widget=widgets.CheckboxInput(),
		verbose_name="Kein Student",
		doc="Ticking the checkbox means that the participant is a non-student.")

	financial_advice = models.BooleanField(
		choices=[(True, "Ja"),(False, "Nein")],
		widget=widgets.RadioSelect(),
		verbose_name="Haben Sie bereits eine Bankberatung in Anspruch genommen?",
		doc="We ask participants if they ever made use of financial advice.")

	income = models.CurrencyField(
		verbose_name="Wie viel Geld im Monat steht Ihnen frei zur Verfügung?",
		doc="We ask participants how much money they have freely available each month.")

	# fields for risk elicitation

	cat_end_rel_1 = models.FloatField(
		doc="Indicates the end point of the first category in relative size.")

	cat_end_rel_2 = models.FloatField(
		doc="Indicates the end point of the second category in relative size.")

	cat_end_rel_3 = models.FloatField(
		doc="Indicates the end point of the third category in relative size.")

	cat_end_rel_4 = models.FloatField(
		doc="Indicates the end point of the fourth category in relative size.")

	cat_end_rel_5 = models.FloatField(
		doc="Indicates the end point of the fifth category in relative size.")

	cat_end_abs_1 = models.PositiveIntegerField(
		doc="Indicates the end point of the first category in pixels.")

	cat_end_abs_2 = models.PositiveIntegerField(
		doc="Indicates the end point of the second category in pixels.")

	cat_end_abs_3 = models.PositiveIntegerField(
		doc="Indicates the end point of the third category in pixels.")

	cat_end_abs_4 = models.PositiveIntegerField(
		doc="Indicates the end point of the fourth category in pixels.")

	cat_end_abs_5 = models.PositiveIntegerField(
		doc="Indicates the end point of the fifth category in pixels.")


# Dummies für Stata:

	female = models.BooleanField(
		doc="Turns True if the participant is a woman."
		)

	male = models.BooleanField(
		doc="Turns True if the participant is a man."
		)

	other_gender = models.BooleanField(
		doc="Turns True if the participant indicates other."
		)

	econ_student = models.BooleanField(
		doc="Turns True if the participant is an economics student."
		)

	follow_customer_1 = models.BooleanField(
		doc="Turns True if the agent chooses the communicated category of his first customer according to his OWN elicited categories."
		)

	follow_customer_2 = models.BooleanField(
		doc="Turns True if the agent chooses the communicated category of his second customer according to his OWN elicited categories."
		)

	follow_customer_3 = models.BooleanField(
		doc="Turns True if the agent chooses the communicated category of his third customer according to his OWN elicited categories."
		)

	follow_customer_4 = models.BooleanField(
		doc="Turns True if the agent chooses the communicated category of his fourth customer according to his OWN elicited categories."
		)

	follow_customer_5 = models.BooleanField(
		doc="Turns True if the agent chooses the communicated category of his fifth customer according to his OWN elicited categories."
		)

	higher_than_customer_1 = models.BooleanField(
		doc="Turns True if the investment of the agent is in a higher category than the one communicated by the first principal according to his OWN elicited categories."
		)

	higher_than_customer_2 = models.BooleanField(
		doc="Turns True if the investment of the agent is in a higher category than the one communicated by the second principal according to his OWN elicited categories."
		)

	higher_than_customer_3 = models.BooleanField(
		doc="Turns True if the investment of the agent is in a higher category than the one communicated by the third principal according to his OWN elicited categories."
		)

	higher_than_customer_4 = models.BooleanField(
		doc="Turns True if the investment of the agent is in a higher category than the one communicated by the fourth principal according to his OWN elicited categories."
		)

	higher_than_customer_5 = models.BooleanField(
		doc="Turns True if the investment of the agent is in a higher category than the one communicated by the fifth principal according to his OWN elicited categories."
		)

	lower_than_customer_1 = models.BooleanField(
		doc="Turns True if the investment of the agent is in a lower category than the one communicated by the principal according to his OWN elicited categories."
		)

	lower_than_customer_2 = models.BooleanField(
		doc="Turns True if the investment of the agent is in a lower category than the one communicated by the principal according to his OWN elicited categories."
		)

	lower_than_customer_3 = models.BooleanField(
		doc="Turns True if the investment of the agent is in a lower category than the one communicated by the principal according to his OWN elicited categories."
		)

	lower_than_customer_4 = models.BooleanField(
		doc="Turns True if the investment of the agent is in a lower category than the one communicated by the principal according to his OWN elicited categories."
		)

	lower_than_customer_5 = models.BooleanField(
		doc="Turns True if the investment of the agent is in a lower category than the one communicated by the principal according to his OWN elicited categories."
		)


	category_from_p1 = models.CharField(
		doc="Category received from every clients first principal."
		)
	category_from_p2 = models.CharField(
		doc="Category received from every clients second principal."
		)
	category_from_p3 = models.CharField(
		doc="Category received from every clients third principal."
		)
	category_from_p4 = models.CharField(
		doc="Category received from every clients fourth principal."
		)
	category_from_p5 = models.CharField(
		doc="Category received from every clients fifth principal."
		)



	def create_gender_dummies(self):
		if self.gender == "weiblich":
			self.female = True
			self.male = False
			self.other_gender = False
		elif self.gender == "männlich":
			self.female = False
			self.male = True
			self.other_gender = False
		elif self.gender == "anderes":
			self.female = False
			self.male = False
			self.other_gender = True

	def create_econ_dummy(self):
		if self.studies:
			subject = self.studies.lower()
			if "econ" in subject:
				self.econ_student = True
			elif "vwl" in subject:
				self.econ_student = True
			elif "ökono" in subject:
				self.econ_student = True
			else:
				self.econ_student = False
		else:
			self.econ_student = False


	def get_categories(self):
		player_list = self.get_others_in_group()
		player_list.append(self)
		player_list.sort(key=lambda p: p.id_in_group)
		# for player in player_list:
		# 	print(player.id_in_group)

		self.category_from_p1=player_list[int(self.c_principal_1)-1].category
		self.category_from_p2=player_list[int(self.c_principal_2)-1].category
		self.category_from_p3=player_list[int(self.c_principal_3)-1].category
		self.category_from_p4=player_list[int(self.c_principal_4)-1].category
		self.category_from_p5=player_list[int(self.c_principal_5)-1].category

	def create_category_dummies_1(self):
		if self.category_from_p1 == "sehr konservativ":
			if 0 <= self.decision_for_p1 < self.cat_end_rel_1*10:
				self.follow_customer_1 = True
				self.higher_than_customer_1 = False
				self.lower_than_customer_1 = False
			else:
				self.follow_customer_1 = False
				if self.decision_for_p1 >= self.cat_end_rel_1*10:
					self.higher_than_customer_1 = True
					self.lower_than_customer_1 = False
				elif self.decision_for_p1 < 0:
					self.lower_than_customer_1 = True
					self.higher_than_customer_1 = False
		if self.category_from_p1 == "sicherheitsorientiert":
			if self.cat_end_rel_1*10 <= self.decision_for_p1 < self.cat_end_rel_2*10:
				self.follow_customer_1 = True
				self.higher_than_customer_1 = False
				self.lower_than_customer_1 = False
			else:
				self.follow_customer_1 = False
				if self.decision_for_p1 >= self.cat_end_rel_2*10:
					self.higher_than_customer_1 = True
					self.lower_than_customer_1 = False
				if self.decision_for_p1 < self.cat_end_rel_1*10:
					self.lower_than_customer_1 = True
					self.higher_than_customer_1 = False
		if self.category_from_p1 == "ausgeglichen":
			if self.cat_end_rel_2*10 <= self.decision_for_p1 < self.cat_end_rel_3*10:
				self.follow_customer_1 = True
				self.higher_than_customer_1 = False
				self.lower_than_customer_1 = False
			else:
				self.follow_customer_1 = False
				if self.decision_for_p1 >= self.cat_end_rel_3*10:
					self.higher_than_customer_1 = True
					self.lower_than_customer_1 = False
				if self.decision_for_p1 < self.cat_end_rel_2*10:
					self.lower_than_customer_1 = True
					self.higher_than_customer_1 = False
		if self.category_from_p1 == "wachstumsorientiert":
			if self.cat_end_rel_3*10 <= self.decision_for_p1 < self.cat_end_rel_4*10:
				self.follow_customer_1 = True
				self.higher_than_customer_1 = False
				self.lower_than_customer_1 = False
			else:
				self.follow_customer_1 = False
				if self.decision_for_p1 >= self.cat_end_rel_4*10:
					self.higher_than_customer_1 = True
					self.lower_than_customer_1 = False
				elif self.decision_for_p1 < self.cat_end_rel_3*10:
					self.lower_than_customer_1 = True
					self.higher_than_customer_1 =False
		if self.category_from_p1 == "offensiv":
			if self.cat_end_rel_4*10 <= self.decision_for_p1 <= 10:
				self.follow_customer_1 = True
				self.higher_than_customer_1 = False
				self.lower_than_customer_1 = False
			else:
				self.follow_customer_1 = False
				if self.decision_for_p1 > 1:
					self.higher_than_customer_1 = True
					self.lower_than_customer_1 = False
				elif self.decision_for_p1 < self.cat_end_rel_4*10:
					self.lower_than_customer_1 = True
					self.higher_than_customer_1 = False

	def create_category_dummies_2(self):
		if self.category_from_p2 == "sehr konservativ":
			if 0 <= self.decision_for_p2 < self.cat_end_rel_1*10:
				self.follow_customer_2 = True
				self.higher_than_customer_2 = False
				self.lower_than_customer_2 = False
			else:
				self.follow_customer_2 = False
				if self.decision_for_p2 >= self.cat_end_rel_1*10:
					self.higher_than_customer_2 = True
					self.lower_than_customer_2 = False
				elif self.decision_for_p2 < 0:
					self.lower_than_customer_2 = True
					self.higher_than_customer_2 = False
		if self.category_from_p2 == "sicherheitsorientiert":
			if self.cat_end_rel_1*10 <= self.decision_for_p2 < self.cat_end_rel_2*10:
				self.follow_customer_2 = True
				self.higher_than_customer_2 = False
				self.lower_than_customer_2 = False
			else:
				self.follow_customer_2 = False
				if self.decision_for_p2 >= self.cat_end_rel_2*10:
					self.higher_than_customer_2 = True
					self.lower_than_customer_2 = False
				if self.decision_for_p2 < self.cat_end_rel_1*10:
					self.lower_than_customer_2 = True
					self.higher_than_customer_2 = False
		if self.category_from_p2 == "ausgeglichen":
			if self.cat_end_rel_2*10 <= self.decision_for_p2 < self.cat_end_rel_3*10:
				self.follow_customer_2 = True
				self.higher_than_customer_2 = False
				self.lower_than_customer_2 = False
			else:
				self.follow_customer_2 = False
				if self.decision_for_p2 >= self.cat_end_rel_3*10:
					self.higher_than_customer_2 = True
					self.lower_than_customer_2 = False
				if self.decision_for_p2 < self.cat_end_rel_2*10:
					self.lower_than_customer_2 = True
					self.higher_than_customer_2 = False
		if self.category_from_p2 == "wachstumsorientiert":
			if self.cat_end_rel_3*10 <= self.decision_for_p2 < self.cat_end_rel_4*10:
				self.follow_customer_2 = True
				self.higher_than_customer_2 = False
				self.lower_than_customer_2 = False
			else:
				self.follow_customer_2 = False
				if self.decision_for_p2 >= self.cat_end_rel_4*10:
					self.higher_than_customer_2 = True
					self.lower_than_customer_2 = False
				elif self.decision_for_p2 < self.cat_end_rel_3*10:
					self.lower_than_customer_2 = True
					self.higher_than_customer_2 =False
		if self.category_from_p2 == "offensiv":
			if self.cat_end_rel_4*10 <= self.decision_for_p2 <= 10:
				self.follow_customer_2 = True
				self.higher_than_customer_2 = False
				self.lower_than_customer_2 = False
			else:
				self.follow_customer_2 = False
				if self.decision_for_p2 > 1:
					self.higher_than_customer_2 = True
					self.lower_than_customer_2 = False
				elif self.decision_for_p2 < self.cat_end_rel_4*10:
					self.lower_than_customer_2 = True
					self.higher_than_customer_2 = False


	def create_category_dummies_3(self):
		if self.category_from_p3 == "sehr konservativ":
			if 0 <= self.decision_for_p3 < self.cat_end_rel_1*10:
				self.follow_customer_3 = True
				self.higher_than_customer_3 = False
				self.lower_than_customer_3 = False
			else:
				self.follow_customer_3 = False
				if self.decision_for_p3 >= self.cat_end_rel_1*10:
					self.higher_than_customer_3 = True
					self.lower_than_customer_3 = False
				elif self.decision_for_p3 < 0:
					self.lower_than_customer_3 = True
					self.higher_than_customer_3 = False
		if self.category_from_p3 == "sicherheitsorientiert":
			if self.cat_end_rel_1*10 <= self.decision_for_p3 < self.cat_end_rel_2*10:
				self.follow_customer_3 = True
				self.higher_than_customer_3 = False
				self.lower_than_customer_3 = False
			else:
				self.follow_customer_3 = False
				if self.decision_for_p3 >= self.cat_end_rel_2*10:
					self.higher_than_customer_3 = True
					self.lower_than_customer_3 = False
				if self.decision_for_p3 < self.cat_end_rel_1*10:
					self.lower_than_customer_3 = True
					self.higher_than_customer_3 = False
		if self.category_from_p3 == "ausgeglichen":
			if self.cat_end_rel_2*10 <= self.decision_for_p3 < self.cat_end_rel_3*10:
				self.follow_customer_3 = True
				self.higher_than_customer_3 = False
				self.lower_than_customer_3 = False
			else:
				self.follow_customer_3 = False
				if self.decision_for_p3 >= self.cat_end_rel_3*10:
					self.higher_than_customer_3 = True
					self.lower_than_customer_3 = False
				if self.decision_for_p3 < self.cat_end_rel_2*10:
					self.lower_than_customer_3 = True
					self.higher_than_customer_3 = False
		if self.category_from_p3 == "wachstumsorientiert":
			if self.cat_end_rel_3*10 <= self.decision_for_p3 < self.cat_end_rel_4*10:
				self.follow_customer_3 = True
				self.higher_than_customer_3 = False
				self.lower_than_customer_3 = False
			else:
				self.follow_customer_3 = False
				if self.decision_for_p3 >= self.cat_end_rel_4*10:
					self.higher_than_customer_3 = True
					self.lower_than_customer_3 = False
				elif self.decision_for_p3 < self.cat_end_rel_3*10:
					self.lower_than_customer_3 = True
					self.higher_than_customer_3 =False
		if self.category_from_p3 == "offensiv":
			if self.cat_end_rel_4*10 <= self.decision_for_p3 <= 10:
				self.follow_customer_3 = True
				self.higher_than_customer_3 = False
				self.lower_than_customer_3 = False
			else:
				self.follow_customer_3 = False
				if self.decision_for_p3 > 1:
					self.higher_than_customer_3 = True
					self.lower_than_customer_3 = False
				elif self.decision_for_p3 < self.cat_end_rel_4*10:
					self.lower_than_customer_3 = True
					self.higher_than_customer_3 = False

	def create_category_dummies_4(self):
		if self.category_from_p4 == "sehr konservativ":
			if 0 <= self.decision_for_p4 < self.cat_end_rel_1*10:
				self.follow_customer_4 = True
				self.higher_than_customer_4 = False
				self.lower_than_customer_4 = False
			else:
				self.follow_customer_4 = False
				if self.decision_for_p4 >= self.cat_end_rel_1*10:
					self.higher_than_customer_4 = True
					self.lower_than_customer_4 = False
				elif self.decision_for_p4 < 0:
					self.lower_than_customer_4 = True
					self.higher_than_customer_4 = False
		if self.category_from_p4 == "sicherheitsorientiert":
			if self.cat_end_rel_1*10 <= self.decision_for_p4 < self.cat_end_rel_2*10:
				self.follow_customer_4 = True
				self.higher_than_customer_4 = False
				self.lower_than_customer_4 = False
			else:
				self.follow_customer_4 = False
				if self.decision_for_p4 >= self.cat_end_rel_2*10:
					self.higher_than_customer_4 = True
					self.lower_than_customer_4 = False
				if self.decision_for_p4 < self.cat_end_rel_1*10:
					self.lower_than_customer_4 = True
					self.higher_than_customer_4 = False
		if self.category_from_p4 == "ausgeglichen":
			if self.cat_end_rel_2*10 <= self.decision_for_p4 < self.cat_end_rel_3*10:
				self.follow_customer_4 = True
				self.higher_than_customer_4 = False
				self.lower_than_customer_4 = False
			else:
				self.follow_customer_4 = False
				if self.decision_for_p4 >= self.cat_end_rel_3*10:
					self.higher_than_customer_4 = True
					self.lower_than_customer_4 = False
				if self.decision_for_p4 < self.cat_end_rel_2*10:
					self.lower_than_customer_4 = True
					self.higher_than_customer_4 = False
		if self.category_from_p4 == "wachstumsorientiert":
			if self.cat_end_rel_3*10 <= self.decision_for_p4 < self.cat_end_rel_4*10:
				self.follow_customer_4 = True
				self.higher_than_customer_4 = False
				self.lower_than_customer_4 = False
			else:
				self.follow_customer_4 = False
				if self.decision_for_p4 >= self.cat_end_rel_4*10:
					self.higher_than_customer_4 = True
					self.lower_than_customer_4 = False
				elif self.decision_for_p4 < self.cat_end_rel_3*10:
					self.lower_than_customer_4 = True
					self.higher_than_customer_4 =False
		if self.category_from_p4 == "offensiv":
			if self.cat_end_rel_4*10 <= self.decision_for_p4 <= 10:
				self.follow_customer_4 = True
				self.higher_than_customer_4 = False
				self.lower_than_customer_4 = False
			else:
				self.follow_customer_4 = False
				if self.decision_for_p4 > 1:
					self.higher_than_customer_4 = True
					self.lower_than_customer_4 = False
				elif self.decision_for_p4 < self.cat_end_rel_4*10:
					self.lower_than_customer_4 = True
					self.higher_than_customer_4 = False


	def create_category_dummies_5(self):
		if self.category_from_p5 == "sehr konservativ":
			if 0 <= self.decision_for_p5 < self.cat_end_rel_1*10:
				self.follow_customer_5 = True
				self.higher_than_customer_5 = False
				self.lower_than_customer_5 = False
			else:
				self.follow_customer_5 = False
				if self.decision_for_p5 >= self.cat_end_rel_1*10:
					self.higher_than_customer_5 = True
					self.lower_than_customer_5 = False
				elif self.decision_for_p5 < 0:
					self.lower_than_customer_5 = True
					self.higher_than_customer_5 = False
		if self.category_from_p5 == "sicherheitsorientiert":
			if self.cat_end_rel_1*10 <= self.decision_for_p5 < self.cat_end_rel_2*10:
				self.follow_customer_5 = True
				self.higher_than_customer_5 = False
				self.lower_than_customer_5 = False
			else:
				self.follow_customer_5 = False
				if self.decision_for_p5 >= self.cat_end_rel_2*10:
					self.higher_than_customer_5 = True
					self.lower_than_customer_5 = False
				if self.decision_for_p5 < self.cat_end_rel_1*10:
					self.lower_than_customer_5 = True
					self.higher_than_customer_5 = False
		if self.category_from_p5 == "ausgeglichen":
			if self.cat_end_rel_2*10 <= self.decision_for_p5 < self.cat_end_rel_3*10:
				self.follow_customer_5 = True
				self.higher_than_customer_5 = False
				self.lower_than_customer_5 = False
			else:
				self.follow_customer_5 = False
				if self.decision_for_p5 >= self.cat_end_rel_3*10:
					self.higher_than_customer_5 = True
					self.lower_than_customer_5 = False
				if self.decision_for_p5 < self.cat_end_rel_2*10:
					self.lower_than_customer_5 = True
					self.higher_than_customer_5 = False
		if self.category_from_p5 == "wachstumsorientiert":
			if self.cat_end_rel_3*10 <= self.decision_for_p5 < self.cat_end_rel_4*10:
				self.follow_customer_5 = True
				self.higher_than_customer_5 = False
				self.lower_than_customer_5 = False
			else:
				self.follow_customer_5 = False
				if self.decision_for_p5 >= self.cat_end_rel_4*10:
					self.higher_than_customer_5 = True
					self.lower_than_customer_5 = False
				elif self.decision_for_p5 < self.cat_end_rel_3*10:
					self.lower_than_customer_5= True
					self.higher_than_customer_5 =False
		if self.category_from_p5 == "offensiv":
			if self.cat_end_rel_4*10 <= self.decision_for_p5 <= 10:
				self.follow_customer_5 = True
				self.higher_than_customer_5 = False
				self.lower_than_customer_5 = False
			else:
				self.follow_customer_5 = False
				if self.decision_for_p5 > 1:
					self.higher_than_customer_5 = True
					self.lower_than_customer_5 = False
				elif self.decision_for_p5 < self.cat_end_rel_4*10:
					self.lower_than_customer_5 = True
					self.higher_than_customer_5 = False