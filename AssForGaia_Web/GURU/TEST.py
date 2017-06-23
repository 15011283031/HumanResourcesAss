import httplib2

http = httplib2.Http()
headers = {}
headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
headers['Accept-Encoding'] = 'deflate'
headers['Accept-Language'] = 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3'
headers['Connection'] = 'keep-alive'
headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0'

needurl = r'http://21.8.143.69:8080/WebReport/ReportServer?reportlet=com.fr.gaia.DefineDatabase&__filename__=[6d4b][8bd5][62a5][8868]'

response,content = http.request(uri = needurl,method = 'get', headers=headers)

print(response)




