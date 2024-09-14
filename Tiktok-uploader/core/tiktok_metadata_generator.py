import random


def get_title():
	# Expanded lists of words for title generation
	adjectives = [
	    "Secret", "Amazing", "Revolutionary", "Unexpected", "Exclusive",
	    "Breakthrough", "Shocking", "Unprecedented", "Profitable", "Innovative",
	    "Advanced", "Inspiring", "Sensational", "Radical", "Iconic"
	]

	topics = [
	    "Bitcoin", "Ethereum", "Ripple", "Litecoin", "Cardano", "DeFi", "NFT", "Blockchain",
	    "Crypto Trading", "Smart Contracts", "Mining", "Staking", "Farming", "DAO", "Metaverse"
	]

	verbs = [
	    "Changes", "Shakes", "Transforms", "Reforms", "Leads",
	    "Revolutionizes", "Dominates", "Overturns", "Redefines", "Influences",
	    "Defines", "Modifies", "Reimagines", "Attracts", "Motivates"
	]

	trends = [
	    "the market", "the industry", "the world of finance", "the crypto community", "the future of trading",
	    "investment strategies", "financial technology", "the digital economy", "asset management",
	    "decentralized applications", "payment systems", "digital identity", "data security",
	    "transaction transparency", "cryptocurrency regulation"
	]

	# More meaningful templates for titles
	templates = [
	    "The {} Revelation: How {} {} {}",
	    "{} {} That {} {}!",
	    "How the {} {} {} {}",
	    "{} {} {} {}: What You Need to Know",
	    "Why {} {} Is the {} {}",
	    "{} {} In The Age Of {}",
	    "Navigating {}: How to {} {} the Game",
	    "The Future Is Here: {} {} and {}",
	    "Insider's Look: The {} Path to {}",
	    "Analysis {}: {} {} and the Future",
	    "{} {} in {}: A Success Story",
	    "The Breakthrough of {}: {} {} in Detail",
	    "The {} Shock: How {} {} Now",
	    "The Era of {}: How {} {} Standards",
	    "The Rise and Fall of {}: The {} Story of {}"
	]


	adjective = random.choice(adjectives)
	topic = random.choice(topics)
	verb = random.choice(verbs)
	trend = random.choice(trends)
	template = random.choice(templates)

	title = template.format(adjective, topic, verb, trend)
	return title


def get_tags():
	tags = [
		"fyp",
	    "crypto",
	    "cryptomash",
	    "cryptocrow",
	    "crypton_x",
	    "cryptosingh1111",
	    "cryptocabin",
	    "cryptocurrency",
	    "cryptotrading",
	    "cryptoreds",
	    "cryptostorepkv",
	    "btc",
	    "btcdaddy",
	    "btchimaghost",
	    "btc_batam",
	    "btcmert",
	    "btcompany",
	    "btchsxz",
	    "btchimacow",
	    "btcmining",
	    "btcburak",	
	    "elonmuskcrypto",
	    "elonmuskdogecoin",
	    "elon_musk",
	    "elonmusk",
	    "cryptonews",
	    "cryptotrading",
	    "cryptolife",
	    "bitcoin",
	    "airdrop",
	    "ethereum",
	    "altcoin",
	    "defi",
	    "trading",
	    "eth",
	    "cryptoinvesting",
	    "recommendations",
	    "recomendation",
	    "wealth",
	    "wealthy"
	]


	return random.sample(tags, 6)




