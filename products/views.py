from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Product
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,get_object_or_404,redirect
from .forms import ProductForm
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from .mixins import LoginRequiredMixin
# de aqui para abajo son los import de pdf generator

import os
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import  TA_CENTER
from reportlab.lib.pagesizes import A4,cm
from reportlab.platypus import Paragraph,Table,TableStyle,Image
from reportlab.lib import colors

this_path = os.getcwd() + '/polls/'
# este es el metodo que crea PDF
def report(request):
	#create the HttpResponse headers with PDF
	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'attachment; filename=Platzi-report.pdf '
	#Create the PDF object, using the BytesIO object as its 'file'
	buffer1 = BytesIO()
	c = canvas.Canvas(buffer1,pagesize=A4)

	#header
	c.setLineWidth(.3)
	c.setFont('Helvetica',22)
	c.drawString(30,750,'Platzi')
	c.setFont('Helvetica',12)
	c.drawString(30,735,'Report')

	c.setFont('Helvetica-Bold',12)
	c.drawString(480,750,'19/01/2018')
	# start x. heightend.  Y. height 
	c.line(460,747,560,747)

	#tabla con datos duumy
	students = [{'#':'1','name':'Miguel Nieva', 'b1':'3.4','b2':'2.2','b3':'4.5','total':'3.36'},
				{'#':'2','name':'Miguelito', 'b1':'3.2','b2':'2.2','b3':'4.2','total':'3.82'},
				{'#':'3','name':'gilberto', 'b1':'3.3','b2':'2.3','b3':'4.3','total':'3.83'},
				{'#':'4','name':'heriberto', 'b1':'3.4','b2':'2.4','b3':'4.4','total':'3.84'},
				{'#':'5','name':'leo negro', 'b1':'3.5','b2':'2.5','b3':'4.5','total':'3.85'},]

	styles = getSampleStyleSheet()
	styleBH = styles["Normal"]
	styleBH.alignment = TA_CENTER
	styleBH.fontSize = 10

	numero = Paragraph('''#''',styleBH)
	alumno = Paragraph('''Alumno''',styleBH)
	b1 = Paragraph('''BIM1''',styleBH)
	b2 = Paragraph('''BIM2''',styleBH)
	b3 = Paragraph('''BIM3''',styleBH)
	total = Paragraph('''Promedio''',styleBH)
	data = []
	data.append([numero, alumno, b1, b2, b3, total ])

	#TABLE 
	styleN = styles["BodyText"]
	styleN.alignment = TA_CENTER
	styleN.fontSize = 7

	high = 650
	for student in students:
		this_student = [student['#'],student['name'],student['b1'],student['b2'],student['b3'],student['total']]
		data.append(this_student)
		high = high - 18 
	#table size
	width, height = A4
	# estos centimetros son los que mide cada columna de cada tabla 
	table = Table(data, colWidths=[1.9 * cm ,9.4 * cm , 1.9 * cm , 1.9 * cm ,1.9 * cm , 2.0 * cm ])
	table.setStyle(TableStyle( [
			('INNERGRID', (0,0) , (-1,1), 0.25, colors.black ),
			('BOX' , (0,0) , (-1,1), 0.25, colors.black ),] ))
	#pdf size
	table.wrapOn(c,width,height)
	table.drawOn(c,30,high)
	c.showPage() #save page

	#save PDF
	c.save()
	#get the value of BytesIO buffer and write response
	pdf = buffer1.getvalue()
	buffer1.close()
	response.write(pdf)
	return response



################ fin del creador de PDFs








@login_required()
def new_product(request):
	if request.method == 'POST':
		form = ProductForm(request.POST, request.FILES)
		if form.is_valid():
			product = form.save(commit=False)
			product.save()
			return HttpResponseRedirect('/')
	else:
		form = ProductForm()
		

	template = loader.get_template('new_product.html')
	context = {
		'form': form
	}
	return HttpResponse(template.render(context,request))

# CLASS BASED VIEWS
class ProductList(ListView):
	model = Product

class ProductDetail(LoginRequiredMixin,DetailView):
	model = Product

def auth_login(request):
	if request.method == 'POST':
		action = request.POST.get('action',None)
		username = request.POST.get('username',None)
		password = request.POST.get('password',None)
		
		if action == 'signup':
			user = User.objects.create_user(username=username,password=password)
			user.save()
		elif action == 'login':
			user = authenticate(username=username,password=password)
			login(request,user)
			return redirect('/')
	context = {}
	return render(request,'login/login.html',context)




		


	