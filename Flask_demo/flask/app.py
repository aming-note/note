#coding:utf8
from flask import Flask,render_template,request,redirect,url_for
from wtforms import Form,TextField,validators
from urllib.parse import unquote
import re,time,os,requests
app = Flask(__name__)
class LoginForm(Form):
    year = TextField("year",[validators.Required()])
    month = TextField("month",[validators.Required()])
    day = TextField("day",[validators.Required()])
    hour = TextField("hour",[validators.Required()])
    min = TextField("min",[validators.Required()])
def get_dig(n,y,r,s,f,filename):
    if filename == "today":
        file = open("C:\\Users\\Admin\\Desktop\\bet.log",'r')
    else:
        file = open("C:\\Users\\Admin\\Desktop\\bak\\bet_2018-08-08_11_34.log",'r')
    code="%s-%s-%s_%s:%s"%(n,y,r,s,f)
    dig_list=[]
    for i in file.readlines():
        if re.findall(r'.*betHistory.*',i):
            continue
        else:
            if re.findall(r'.*%s.*'%code,i):
                zhudan=[]
                ziduan=re.split(r',',i)
                for s in ziduan:
                    if re.findall(r'unique=.*',s):
                        danhao=re.split(r'&',s)
                        for c in danhao:
                            if re.findall(r'bets.*',c):
                                neirong=re.split(r'=',c)
                                zhuan="bets=%s"%unquote(neirong[1],'utf-8')
                                zhudan.insert(-1,zhuan)
                            else:
                                zhudan.insert(-1,c)
                    elif re.findall(r"^\"\d+.\d+.\d+.\d+",s) and not re.findall(r".*-.*_.*:",s):
                        ip = re.split(r"\"",s)
                        get = requests.get("https://ip.cn/index.php?ip=%s"%ip[1]).content.decode()
                        res = re.findall(r".*所在地理位置.*",get)
                        geo_sp = re.split(r"code",str(res))
                        geo = re.split(r"[>,<]",geo_sp[3])
                        zhudan.insert(-1,"%s:%s"%(s,geo[1]))
                    else:
                        zhudan.insert(-1,s)
                dig_list.insert(-1,zhudan)
    return dig_list
@app.route('/',methods=['GET','POST'])
def index():
    myForm = LoginForm(request.form)
    if request.method == 'POST':
        year = myForm.year.data
        month = myForm.month.data
        day = myForm.day.data
        hour = myForm.hour.data
        fen = myForm.min.data
        if "%s-%s-%s"%(year,month,day) == time.strftime("%Y-%m-%d"):
            print(1)
            data = get_dig(year, month, day, hour, fen, 'today')
            if data:
                return render_template('index.html', data=data, form=myForm)
            else:
                return render_template('index.html', data="no", form=myForm)
        else:

            lst = os.listdir('C:\\Users\\Admin\\Desktop\\bak')
            for f in lst:
                if not os.path.isdir(f):
                    if re.findall(r'.*\.log',f):
                        file_name = "C:\\Users\\Admin\\Desktop\\bak\\%s"%f
                        data = get_dig(year, month, day, hour, fen, file_name)
                        if data:
                            return render_template('index.html', data=data, form=myForm)
                        else:
                            return render_template('index.html', data="no", form=myForm)
            return render_template('index.html', data="no", form=myForm)
    return render_template('index.html', form=myForm)

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
