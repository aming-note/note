from flask import Flask,render_template,request,redirect,url_for
from wtforms import Form,TextField,validators
from urllib.parse import unquote
import re,datetime,os
app = Flask(__name__)
class LoginForm(Form):
    year = TextField("year",[validators.Required()])
    month = TextField("month",[validators.Required()])
    day = TextField("day",[validators.Required()])
    hour = TextField("hour",[validators.Required()])
    min = TextField("min",[validators.Required()])
def get_dig(n,y,r,s,f,filename):
    file = open(filename,'r')
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
        min = myForm.min.data
        if "%s-%s-%s"%(year,month,day) == datetime.datetime.today():
            data = get_dig(year, month, day, hour, min, '/usr/local/nginx/logs/bet.log')
            return render_template('index.html', data=data, form=myForm)
        else:
            lst = os.listdir('/home/log_bak')
            for f in lst:
                if not os.path.isdir(f):
                    if re.findall(r'bet_%s-%s-%s_.....\.log'%(year,month,day),f):
                        data = get_dig(year, month, day, hour, min, f)
                        return render_template('index.html', data=data, form=myForm)
                    else:
                        return render_template('index.html', data="no", form=myForm)
                else:
                    return render_template('index.html', data="no", form=myForm)
    return render_template('index.html',form=myForm)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=7788)