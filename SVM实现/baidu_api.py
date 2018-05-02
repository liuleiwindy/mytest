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

	def classify_emotion(self, text):
		res = self.client.sentimentClassify(text)['items'][0]
		print(res)
		confidence = res['confidence']
		sentiment = res['sentiment']
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



text = "苹果是一家伟大的公司"

if __name__ == '__main__':
	api = baidu_sentiment_analyze()
	# api.classify_emotion(text)
	api.load_text(api.csv_file)
	api.write_csv()
