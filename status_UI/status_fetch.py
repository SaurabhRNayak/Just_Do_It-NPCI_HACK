from flask import Flask,request,render_template,Response
from pymongo import MongoClient


app=Flask(__name__)
def connect_mongo():
    global client,db,complaint_reg
    client = MongoClient('mongodb://localhost:27017')
    db = client['Database']
    complaint_reg = db.complaint_reg
    print("/*")

@app.route('/home',methods=['GET','POST'])
def check():
    print(request.form["options"])
    if request.form["options"]=="Register Complaint":
        return render_template("new_complaint.html")
    if request.form["options"]=='Get Status':
        return render_template("get_complaint id.html")
    else:
        return render_template("home.html")


@app.route('/',methods=['POST','GET'])
def channel():
    print("/")
    return render_template("home.html")

@app.route('/new_complaint',methods=['POST','GET'])
def new_comp():
    consumer_id =request.form["cons_id"]
    trans_id = request.form["trans_id"]
    desc = request.form["desc"]
    temp = (complaint_reg.find().sort([("_id", -1)]).limit(1))
    comp_id=temp[0]['comp_id']+1
    complaint_reg.insert_one({'comp_id':comp_id,"consumer_id":consumer_id,"trans_id":trans_id,"desc":desc,"govt":"N","bank":"N","active":"Y"})

    return render_template("display.html",comp_id=comp_id)

@app.route('/status',methods=['POST','GET'])
def abc():
    comp_id = request.form['comp_id']
    print(complaint_reg.find())
    result=(complaint_reg.find_one({"comp_id":int(comp_id)}))
    print(result)
    f1=None
    f2=None
    print(result['govt'])
    if result['govt'].lower()=='y':
        print(123)
        f1='completed'
        if result['bank'].lower() == 'y':
            print(456)
            f2 = 'completed'
    return render_template("step_status_bar.html",stat1=f1,stat2=f2)
if __name__=='__main__':
    connect_mongo()
    # abc()
    app.run()