# -*- coding: utf-8 -*-
import csv, re, jieba, time
import warnings
import logging

# jieba.enable_parallel(4)
# MYSQL_HOSTS = 'localhost'
# MYSQL_USER = 'ROOT'
# MYSQL_PASSWORD = 'ROOT'
# MYSQL_PORT = '3306'
# MYSQL_DB = 'test'

text = '#创以智用，与人工智能-同行#每天都在用的siri就是最大的改变了，天天早上起来都会问一下今天的天气[bm思考][鲜花]。-@商汤SenseTime#创以智用,与人工智能-同行#AI浪潮来袭，SenseTimeInside带来产业升级！4月25日，2018商汤人工智能大会将震撼登场，汇聚最前沿的AI技术，解锁最契合的产业方案，一起creAIte！美颜拍照更自然、芯片性能更高效、社交互动更好玩、购物体验更前卫……AI正在为改变全人类的美好生活而努力！参与话题互动...展开全文c转发1910-评论67--28-<ahref="//weibo.com/5477684004/GdpE8jrpt?refer_flag=1001030103_"    '

class pre_processing(object):
	"""docstring for pre_processingg"""
	def __init__(self):
		super(pre_processing, self).__init__()
		self.csv_file = '/Users/Penicillin666/Documents/毕业设计/数据爬取/SinaSpider/weibo/result-0425.csv'
		self.SougouW = csv.reader(open('SogouLabDic.csv', 'r', encoding='utf-8'))
		self.freq_dic = [row[0] for row in self.SougouW]
		self.stopwords_path = 'stopwords0000.txt'
		self.all_sentences = ''
		self.list_sentences = []

	def del_noise(self, text):
		noise_pattern = re.compile(r'(?:回复)?(?://)?(@[\w\u2E80-\u9FFF]+:?)|#.+?#|(\\/)+|\.{3}|&quot;|&gt;|\d+|[a-zA-Z]+|网页链接|\n+|\s+|转发微博|&amp;|-*转发\d+-*评论\d+-*\d+|-<ahref.+|展开全文')
		emoti_pattern = re.compile(r'\[([\u4e00-\u9fa5]|\w){1,4}\]')
		exclaim_pattern = re.compile(r'\!|\?|\！|\？')
		emotis = [x.group(0)[1:-1] for x in emoti_pattern.finditer(text)]
		clean_text = noise_pattern.sub(r'', text).replace('--', '')
		clean_text = emoti_pattern.sub(r'', clean_text)
		exclaims = exclaim_pattern.findall(clean_text)
		return [clean_text, emotis, len(exclaims)]

	def sentence_cut(self, text):
		num_pa = re.compile(r'\d+')
		text = num_pa.sub(r'', text)
		res = self.jiebaclearText(text).replace('/', ' ') +'\n'
		if not res in self.list_sentences:
			self.list_sentences.append(res)
			self.all_sentences += res

	def write_train_input(self):
		csv_read = csv.reader(open(self.csv_file, 'r', encoding='utf-8'))
		input_list = list(csv_read)

		# input_list.sort()
		# for i in range(1, 200, 10):
		for row in input_list:
			clean_text = self.del_noise(row[2])[0]
			self.sentence_cut(clean_text)
		with open('train_input.txt', 'w+', encoding='utf-8') as f:
			f.write(self.all_sentences)

	def jiebaclearText(self, text):
		mywordlist = []
		seg_list = jieba.cut(text, cut_all = False, HMM = True)
		liststr = '/'.join(seg_list)
		f_stop = open(self.stopwords_path, encoding = 'utf-8')
		try:
			f_stop_text = f_stop.read()
		finally:
			f_stop.close()
		f_stop_seg_list = f_stop_text.split('\n')
		for myword in liststr.split('/'):
			if not (myword.strip() in f_stop_seg_list ) and len(myword.strip())>1:
				mywordlist.append(myword)
		return '/'.join(mywordlist)

if __name__ == '__main__':
	start_time = time.time()
	p = pre_processing()
	# clean_text = p.del_noise(text)[0]
	# p.sentence_cut(clean_text)
	p.write_train_input()
	end_time = time.time()
	print('Time costing %f' % (end_time - start_time))
	print(len(p.list_sentences))
