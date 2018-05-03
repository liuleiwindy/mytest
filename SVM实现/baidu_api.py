from aip import AipNlp
import csv, re, codecs


APP_ID = '11177799'
API_KEY = 'irBhn2owG60zUaoHjlGjuZwV'
SECRET_KEY = 'C6RBeUtPflwAa8iaiGFqGLUErCbQIu1v'

class baidu_sentiment_analyze(object):
	"""docstring for baidu_sentiment_analyze"""
	def __init__(self):
		super(baidu_sentiment_analyze, self).__init__()
		self.client = AipNlp(APP_ID, API_KEY, SECRET_KEY)
		self.csv_file = 'result-0425.csv'
		self.rows = []
		self.hotel_file = '2000/'

	def classify_emotion(self, text):
		try:
			res = self.client.sentimentClassify(text)['items'][0]
			confidence = res['confidence']
			sentiment = res['sentiment']
		except:
			print('failed')
			sentiment = 1
		if sentiment != 1 and confidence < 0.5:
			sentiment = 1
		return sentiment

	def del_noise(self, text):
		noise_pattern = re.compile(r'(?:回复)?(?://)?(@[\w\u2E80-\u9FFF]+:?)|\[\w+\]|#.+?#|网页链接|\.+|\n*|\s*|转发\d+-评论\d+--\d+-<ahref.+|...展开全文')
		emoti_pattern = re.compile(r'\[([\u4e00-\u9fa5]+|\w+)+?\]')
		exclaim_pattern = re.compile(r'\!|\?|\！|\？')
		emotis = list(set(emoti_pattern.findall(text)))
		clean_text = noise_pattern.sub(r'', text)
		exclaims = exclaim_pattern.findall(clean_text)
		return [clean_text, emotis, len(exclaims)]

	def write_csv(self):
		f = codecs.open('test.csv', 'w', encoding='utf_8_sig')
		csv_writer = csv.writer(f)
		for row in self.rows:
			csv_writer.writerow(row)

	def load_text(self, csv_file):
		f = open(csv_file, 'r', encoding='utf-8')
		csv_reader = csv.reader(f)
		l_csv = list(csv_reader)
		for row in l_csv[:10]:
			clean_text = self.del_noise(row[2])[0]
			sentiment = self.classify_emotion(clean_text)
			self.rows.append(row[:2] + [clean_text] + [sentiment])
			print(self.rows[-1])

	def load_hotel_text(self):
		neg_file = []
		pos_file = []
		for file_name in ['neg', 'pos']:
			for i in range(1000):
				value = {
				'all_file': self.hotel_file,
				'category': file_name,
				'num': i
				}
				file = '%(all_file)s%(category)s/%(category)s.%(num)d.txt' % value
				with open(file, 'r', encoding='utf-8') as f:
					if file_name == 'neg':
						neg_file.append(f.read())
					else:
						pos_file.append(f.read())
					f.close()
		res = {'neg': neg_file, 'pos': pos_file}
		return res

	def hotel_judge(self, res_dic):
		negs = 0.0
		poss = 0.0
		neg_num = len(res_dic['neg'])
		pos_num = len(res_dic['pos'])
		for item in res_dic.items():
			for text in item[1]:
				sentiment = self.classify_emotion(text)
				if item[0] == 'neg' and sentiment == 0:
					negs += (sentiment + 1) # barely count the number of sentiment since negative's sentiment is 0 judged by baiduapi
				elif item[0] == 'pos' and sentiment == 2:
					poss += (sentiment - 1)
		neg_precise = negs / neg_num
		pos_precise = poss / pos_num
		print(negs, poss)
		print(neg_precise, pos_precise)

text = "苹果是一家伟大的公司"

if __name__ == '__main__':
	api = baidu_sentiment_analyze()
	# api.classify_emotion(text)
	# api.load_text(api.csv_file)
	# api.write_csv()
	res = api.load_hotel_text()
	api.hotel_judge(res)
