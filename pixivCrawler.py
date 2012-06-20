from BeautifulSoup import BeautifulSoup
import urllib2,urllib,os,time

folder_root = 'D:\pixiv'

year = time.strftime('%Y',time.localtime(time.time()))
month = time.strftime('%m',time.localtime(time.time()))
day = time.strftime('%d',time.localtime(time.time()))
folder_time = year+'-'+month+'-'+day

def download(mode,page):
	url = 'http://www.pixiv.net/ranking.php?mode='+mode+'&p='+page
	page = urllib2.urlopen(url)
	soup = BeautifulSoup(page)
	a = soup.findAll('a','image-thumbnail')
	a_num = len(a)
	rank = soup.findAll('div','rank')

	for i in range(0,a_num):
		ranknum = rank[i].find('h1').find('a')['href']
		ranknum = ranknum.replace('#','')
		ranknum = '%03d'%( int(ranknum) )
		each_a = a[i]
		imgurl = each_a.find('img')['data-src']
		imgurl = imgurl.split('?')
		imgurl = imgurl[0]
		imgurl = imgurl.replace('_s','')
		imgid = imgurl[-12:-4]
		artistid = imgurl[27:-13]
		imghost = imgurl[10:12]
		imgtype = imgurl[-3:]

		if os.path.exists(folder_root):
			pass
		else:
			os.mkdir(folder_root)
		if os.path.exists(folder_root+'\\'+mode):
			pass
		else:
			os.mkdir(folder_root+'\\'+mode)
		if os.path.exists(folder_root+'\\'+mode+'\\'+folder_time):
			pass
		else:
			os.mkdir(folder_root+'\\'+mode+'\\'+folder_time)
		
		wget = 'wget '+imgurl+' -O '+folder_root+'\\'+mode+'\\'+folder_time+'/'+ranknum+'-'+artistid+'-'+imgid+'-'+imghost+'.'+imgtype+' --referer=http://www.pixiv.net/'
		status = os.system(wget)

		if status == 1:
			url_new = 'http://www.pixiv.net/member_illust.php?mode=manga&illust_id='+imgid
			page_new = urllib2.urlopen(url_new)
			soup_new = BeautifulSoup(page_new)
			imgs_new = soup_new.findAll('div','image-container')
			img_num = len(imgs_new)

			for i in range(0,img_num):
				imgid_new = imgid+'_p'+str(i)
				imgurl_new = imgurl.replace(imgid,imgid_new)
				wget = 'wget '+imgurl_new+' -O '+folder_root+'\\'+mode+'\\'+folder_time+'/'+ranknum+'-'+artistid+'-'+imgid_new+'-'+imghost+'.'+imgtype+' --referer=http://www.pixiv.net/'
				os.system(wget)
			os.remove(folder_root+'\\'+mode+'\\'+folder_time+'/'+ranknum+'-'+artistid+'-'+imgid+'-'+imghost+'.'+imgtype)

for i in range(1,3):
	download('monthly',str(i))
	download('weekly',str(i))
	download('daily',str(i))