import requests
import sys
import json

textWrite=True
is_pydroid=False
if(is_pydroid):
    arg="python yxpHw 1585732 语文".split(" ")
else:
    arg=sys.argv
def yxpTimeGet():
    urlT="http://e.anoah.com/api_dist/?q=json/ebag/System/getServerTime&info={}"
    out=requests.get(urlT)
    out=json.loads(out.text)
    return out["recordset"]["system_time"]
def yxpName(uid):
    urlN="https://e.anoah.com/api/?q=json/ebag/user/score/score_rank&info={\"userid\":%s}&pmatsemit=%s"%(uid,str(yxpTimeGet()))
    return json.loads(requests.get(urlN).text)["recordset"]["real_name"]
def yxpClassId(uid):
    urlClass="https://e.anoah.com/api/?q=json/ebag5/User/getUserClasses&info={\"userid\":%s}&pmatsemit=%s"%(uid,yxpTimeGet())
    Class=json.loads(requests.get(urlClass).text)
    ClassScore=""
    for t in range(0,len(Class["recordset"])):
        if t==0:
            ClassScore=Class["recordset"][t]["class_id"]
        else:
            ClassScore=str(ClassScore)+","+str(Class["recordset"][t]["class_id"])
    return ClassScore
####################################################### 
if len(arg)==3:
    if arg[1]=="yxpDCom":
        url="http://e.anoah.com/api_cache/?q=json/icom/Dcom/getDCom&info={\"dcom_id\":%s}"%int(arg[2])
        print(url)
        out=requests.get(url)
        out=json.loads(out.text)
        if "status" in out:
            text="指定的作业不存在"
        else:
            text="""优学派作业ID：%s    
创建时间：%s    
作业名称：%s    
作业标题：%s    
活动名称：%s    
描述：%s"""%(str(out["id"]),str(out["create_time"]),str(out["dcom_name"]),str(out["dcom_title"]),str(out["activity_name"]),str(out["description"]))
####################################################### 
    elif arg[1]=="yxpPic":
        url="https://e.anoah.com/api/?q=json/ebag/user/score/score_rank&info={\"userid\":%s}&pmatsemit=%s"%(arg[2],str(yxpTimeGet()))
        out=requests.get(url)
        out=json.loads(out.text)
        urlPic="http://static.anoah.com"
        urlJson=out["recordset"]["avatar"]
        urlJson=urlJson.replace(r"\/","/")
        if(urlJson.startswith("http")):
            urlPic=urlJson
            urlPic2="http://www.anoah.com/ebag/static/images/noavatar.jpg"
        else:
            urlPic=urlPic+urlJson
            urlPic2=urlPic.replace(".jpg","_private.jpg")
        Pic=requests.get(urlPic)
        with open(r"D:\Program Source\QQBOT\python\Temp\FacePublic.jpg","wb+") as f:
            f.write(Pic.content)
        Pic2=requests.get(urlPic2)
        with open(r"D:\Program Source\QQBOT\python\Temp\FacePrivate.jpg","wb+") as f:
            f.write(Pic2.content)
        text=yxpName(arg[2])
#######################################################
    elif arg[1]=="yxpInfo":
        time=yxpTimeGet()
        urlHaoTiBen="https://e.anoah.com/api/?q=json/ebag5/Qtibook/readBookStatus&info="\
            "{\"start_time\":\"2008-08-08+00:00:00\",\"user_id\":%s}&pmatsemit=%s"%(arg[2],time)
        urlClass="https://e.anoah.com/api/?q=json/ebag5/User/getUserClasses&info={\"userid\":%s}&pmatsemit=%s"%(arg[2],time)
        urlScore="https://e.anoah.com/api/?q=json/ebag/user/score/score_rank&info={\"userid\":%s}&pmatsemit=%s"%(arg[2],time)
        urlScore2="https://e.anoah.com/api/?q=json/ebag/user/score/score_count&info={\"userid\":%s}"%arg[2]
        urlScore3="https://e.anoah.com/api/?q=json/ebag/user/score/score_detail&info"\
            "={\"userid\":%s,\"pagesize\":10,\"page\":1,\"start\":\"\",\"end\":\"\"}&pmatsemit=%s"%(arg[2],time)
        HaoTi=json.loads(requests.get(urlHaoTiBen).text)
        Class=json.loads(requests.get(urlClass).text)
        ClassScore=""
        for t in range(0,len(Class["recordset"])):
            if t==0:
                ClassScore=Class["recordset"][t]["class_id"]
            else:
                ClassScore=str(ClassScore)+","+str(Class["recordset"][t]["class_id"])
        urlClassIn="https://api2.anoah.com/jwt/user/classes/subjects?class_id=%s&pmatsemit=%s"%(ClassScore,time)
        urlHomework="https://e.anoah.com/api/?q=json/ebag5/Homework/readHomeworkStat&info="\
            "{\"to\":\"\",\"class_ids\":\"%s\",\"user_id\":%s,\"from\":\"\"}&pmatsemit=%s"%(ClassScore,arg[2],time)
        Score=json.loads(requests.get(urlScore).text)
        Score2=json.loads(requests.get(urlScore2).text)
        Score3=json.loads(requests.get(urlScore3).text)
        ClassIn=json.loads(requests.get(urlClassIn).text)
        Homework=json.loads(requests.get(urlHomework).text)
        #---------------------------------------------
####################################################### 
elif len(arg)==2:
    if arg[1]=="yxpTIME": 
        text=yxpTimeGet()
    elif arg=="yxpJWT":
        urln="https://emessage.anoah.com/api/?q=json/jwt/Emessage/get_list_latest&info="\
            "{\"message_types\":\"0,1,2\",\"user_id\":1585732}&pmatsemit="+str(yxpTimeGet())
        outn=requests.get(urln)
        text=outn.text
    else:
        text="Error"
#######################################################
elif len(arg)==4:
    if arg[1]=="yxpRs":
        Classid=yxpClassId(arg[2])
        if(arg[3]=="最新"):
            subjectlist=[1,2,3,4,5,6,7,8,32,33,14,23,437]
            subjectNamelist=["语文","数学","英语","化学（测试性功能）",'历史','地理','生物','物理','美术','信息','音乐','体育','道法']
            text="这是 "+yxpName(arg[2])+"的全科最近分数（仅显示已批改）：\n"
            for i in range(0,13):
                url="http://e.anoah.com/api/?q=json/ebag5/Statistics/getStudentScoreInfo&info="\
                    "{\"user_id\":%s,\"class_id\":\"%s\",\"type\":0,\"subject_id\":%s,\"pagesize\":10,\"page\":1,\"start_date\":\"\",\"end_date\":\"\"}&pmatsemit=%s"%(arg[2],Classid,subjectlist[i],yxpTimeGet())
                out=json.loads(requests.get(url).text)
                if(out["recordset"]==""):
                    text=text+"☛ "+subjectNamelist[i]+"：无 已批改 成绩\n"
                else:
                    if(i in range(0,3)):
                        result=round(out["recordset"][0]["student_right_rate"]*120,2)
                        classr=round(out["recordset"][0]["class_right_rate"]*120,2)
                    else:
                        result=round(out["recordset"][0]["student_right_rate"]*100,2)
                        classr=round(out["recordset"][0]["class_right_rate"]*100,2)
                    if(result>=classr):
                        string="■"
                    else:
                        string="□"
                    text=text+"☛ "+subjectNamelist[i]+"："+out["recordset"][0]["publish_time"]+" "+out["recordset"][0]["title"]+"\n个人："+\
                        str(result)+"分（"+str(out["recordset"][0]["student_right_rate"])+"）\n全班平均分："+\
                        str(classr)+"分（"+str(out["recordset"][0]["class_right_rate"])+"）  "+string+"\n"
        #---------------------------------------------
        else:
            if  (arg[3]=="语文"):subjectId=1 #
            elif(arg[3]=="数学"):subjectId=2 #
            elif(arg[3]=="英语"):subjectId=3 #
            elif(arg[3]=="历史"):subjectId=5 #
            elif(arg[3]=="地理"):subjectId=6
            elif(arg[3]=="生物"):subjectId=7 #
            elif(arg[3]=="物理"):subjectId=8
            elif(arg[3]=="美术"):subjectId=32
            elif(arg[3]=="信息"):subjectId=33
            elif(arg[3]=="音乐"):subjectId=14
            elif(arg[3]=="体育"):subjectId=23
            elif(arg[3]=="道法"):subjectId=437
            url="http://e.anoah.com/api/?q=json/ebag5/Statistics/getStudentScoreInfo&info={\"user_id\":%s,\"class_id\":\"%s\",\"type\":0,\"subject_id\":%s,\"pagesize\"10,\"page\":1,\"start_date\":\"\",\"end_date\":\"\"}&pmatsemit=%s"%(arg[2],yxpClassId(arg[2]),subjectId,yxpTimeGet())
#######################################################
    if arg[1]=="yxpHw":
        time=yxpTimeGet()
        #---------------------------------------------
        if  (arg[3]=="语文"):subjectId=1 #
        elif(arg[3]=="数学"):subjectId=2 #
        elif(arg[3]=="英语"):subjectId=3 #
        elif(arg[3]=="历史"):subjectId=5 #
        elif(arg[3]=="地理"):subjectId=6
        elif(arg[3]=="生物"):subjectId=7 #
        elif(arg[3]=="物理"):subjectId=8
        elif(arg[3]=="美术"):subjectId=32
        elif(arg[3]=="信息"):subjectId=33
        elif(arg[3]=="音乐"):subjectId=14
        elif(arg[3]=="体育"):subjectId=23
        elif(arg[3]=="道法"):subjectId=437
        #---------------------------------------------
        urlNOK="http://api2.anoah.com/jwt/homework/publish/getListForStudent?user_id=%s&status=0&subject_id=%s&class_id=%s&from_date=&to_date=&page=1&per_page=20&pmatsemit=%s"%(arg[2],str(subjectId),yxpClassId(arg[2]),time)
        urlOk="http://api2.anoah.com/jwt/homework/publish/getListForStudent?user_id=%s&status=1&subject_id=%s&class_id=%s&from_date=&to_date=&page=1&per_page=20&pmatsemit=%s"%(arg[2],str(subjectId),yxpClassId(arg[2]),time)
        ok=json.loads(requests.get(urlOk).text.encode('utf-8').decode("unicode_escape"))
        nok=json.loads(requests.get(urlNOK).text.encode('utf-8').decode("unicode_escape"))
        if(ok["status"]==0):
            text=ok["msg"]
        else:
        #---------------------------------------------
            okjs=ok["recordset"]
            nokjs=nok["recordset"]
            text="这是"+yxpName(arg[2])+"的"+arg[3]+"作业情况：\n"
            lists=okjs["lists"]
            noklists=nokjs["lists"]
            write=1
            if(okjs["total_count"]==0):
                text="没有写了的作业。\n"
                write=0
            else:
                if(int(okjs["total_count"])>int(okjs["per_page"])):
                    rg=okjs["per_page"]
                else:
                    rg=okjs["total_count"]
                for i in range(0,int(rg)):
                    if i==0:
                        text=text+"☛ 写了的作业（%s个）：\n"%(okjs["total_count"])
                    text=text+lists[i]["start_time"]+" "+lists[i]["title"]+" "+lists[i]["subject_name"]+lists[i]["teacher_name"]#+"\n作业ID："+lists[i]["course_hour_publish_id"]
                    if not i==int(okjs["total_count"]):
                        text=text+"\n"
                if (int(okjs["per_page"])<int(okjs["total_count"])):
                    text=text+"※ 仅显示%s个，但一共有%s个作业完成\n"%(int(okjs["per_page"]),int(okjs["total_count"]))
            if(nokjs["total_count"]==0):
                if(write==0):
                    text="老师没留过作业。"
                else:
                    text=text+"没有没写的作业。"
            else:
                if(int(nokjs["total_count"])>int(nokjs["per_page"])):
                    rg=nokjs["per_page"]
                else:
                    rg=nokjs["total_count"]
                for i in range(0,int(rg)):
                    if i==0:
                        text=text+"☛ 没写的作业（%s个）：\n"%(nokjs["total_count"])
                    text=text+noklists[i]["start_time"]+" "+noklists[i]["title"]+" "+noklists[i]["subject_name"]+noklists[i]["teacher_name"]#+"\n作业ID："+noklists[i]["course_hour_publish_id"]
                    if not i==int(okjs["total_count"]):
                        text=text+"\n"
                if (int(nokjs["per_page"])<int(nokjs["total_count"])):
                    text=text+"※ 仅显示%s个，但一共有%s个作业未完成"%(int(nokjs["per_page"]),int(nokjs["total_count"]))
#######################################################
else:
    text="参数不够"
####################################################### 
with open(r"D:\Program Source\QQBOT\python\Temp\temp.txt","w+",encoding="UTF-8") as f:
    if(textWrite):
        text=str(text)
        f.write(text)
        print(text)
