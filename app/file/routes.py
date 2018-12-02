import os
from os import listdir
from os.path import isfile, join
from flask import send_file
import pandas as pd
from app.pandaex import  sendpandas
from app.file import bp
from flask_login import login_required
import requests
from requests import Request, Session
from flask import render_template, flash, redirect, url_for, request, g, current_app, json
from flask_babel import _, get_locale
from werkzeug.utils import secure_filename
import openpyxl
from openpyxl import load_workbook




UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER_ENV')
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'xlsx','cfg'])
ALLOWED_EXTENSIONS_PANDAS = set(['xlsx'])
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def allowed_file_pandas(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_PANDAS
    return True  






@bp.route('/uploads', methods=['GET', 'POST'])
@login_required
def uploads():
    list=[]
    for x in os.listdir(UPLOAD_FOLDER):
        list.append(x)
    print(list)

        
    

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            flash(_('File uploaded!'))
            #if allowed_file_pandas(file.filename):
                #sendpandas(filename)
                
          

            
        return redirect(url_for('file.uploads',
                            filename=filename, ))
       

    
    return render_template('uploads.html', title=_('Uploads'), list=list)


@bp.route('/return_files/<filename>')
def return_files(filename):
    try:
        return send_file(UPLOAD_FOLDER+filename , attachment_filename=filename)
    except Exception as e:
        return str(e)
    return render_template('uploads.html', title=_('Uploads'), list=list)






@bp.route('/expy',methods=['GET', 'POST'])
@login_required




def expy(cat,scat,hard,user,tech,cust,contr,time):

    
    sheet=cat
    print(cat)
    srcfile = openpyxl.load_workbook(os.environ.get('EXCEL_FOLDER_ENV'),read_only=False)
    sheetname = srcfile.get_sheet_by_name(sheet)
    save("A",tech, sheetname)
    save("B",cust, sheetname)
    save("C",contr, sheetname)
    save("D",hard, sheetname)
    save("E",time, sheetname)
    save("F",user, sheetname)
    save("G",scat, sheetname)


    srcfile.save(os.environ.get('EXCEL_FOLDER_ENV'))

    



def save(l, t,sheetname):
    
    
    for cell in sheetname[l]:
        
        if cell.value is None:
            break
        empty_row =(cell.row)+1
            

         
    if not t:
        print('Object is none')

        sheetname[l+"%d"  % empty_row]= str("/")
        return True
    sheetname[l+"%d"  % empty_row]= str(t)


