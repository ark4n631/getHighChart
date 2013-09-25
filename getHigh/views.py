# -*- coding: utf-8 -*-
from django.views.decorators.csrf import csrf_exempt
from collections import OrderedDict
from django.conf import settings
from django.shortcuts import render,render_to_response,redirect
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.template import RequestContext

import simplejson,ast

def index(request):
	host = 'http://'+request.META['HTTP_HOST'] + request.path
	return render(
		request,
		'index.html',
		{'host':host},
		context_instance=RequestContext(request)
		)

"""
	createdBy : Esteban Fuentealba F. (@rk4n631)
	getGraph : return json object 
		on error return json object =>
		{
			errors : []
		}
	input (trhough URL) : 
		type : (type of graph) [line,column,bar,pie] (at the moment) | string needed
		catX : (categories) [cat1,cat2,cat3,catN] | list needed
		catY : (categories) [cat1,cat2,cat3,catN] | list optional
		names : (names of series) [serie1,serie2,serieN] | list needed
		title : (title of the graph) string or None optional
		values : (list inside list of values eg: [[(serie1)1,2,3],[(serie2)4,5,6]]) [n[],n*[n]] | list[] inside list[] need
		metricX : (metric system of X eg: °C, KM) string or None optional
		metricY : (metric system of Y axe eg: #People,$US) string or None optional

"""
@csrf_exempt
def getGraph(request):
	reqDict = request.GET
	errorTipo = []
	errors = {'errors':[]}
	error = False
	nombres = []
	tipoGraph = ''
	valores = []
	chart = OrderedDict({'chart':{'type':''},'title':{'text':None},'xAxis':{'title':{'text':None},'categories':[]},'yAxis':{'title':{'text':None}}})
	if(reqDict.__contains__('type')):
		if(reqDict.get('type')=='line'):
			chart['chart']['type']='line'
			tipoGraph='line'
		elif(reqDict.get('type')=='column'):
			chart['chart']['type']='column'
			tipoGraph='column'
		elif(reqDict.get('type')=='pie'):
			del(chart['chart']['type'])
			tipoGraph='pie'
		elif(reqDict.get('type')=='bar'):
			chart['chart']['type']='bar'
			tipoGraph='bar'
	else:
		error = True
		errorTipo.append('Debe especificar el tipo de gráfico en type')
	if(reqDict.__contains__('catX[]')):
		chart['xAxis']['categories']=reqDict.getlist('catX[]')
	else:
		error = True
		errorTipo.append('Debe adjuntar las categorias como catX si es en el ejeX o catY si es en el ejeY')
	if(reqDict.__contains__('metricX')):
		chart['xAxis']['title']['text']=reqDict.get('metricX')
	if(reqDict.__contains__('metricY')):
		chart['yAxis']['title']['text']=reqDict.get('metricY')
	if(reqDict.__contains__('title')):
		chart['title']['text'] = reqDict.get('title')
	if(reqDict.__contains__('names[]')):
		nombres = reqDict.getlist('names[]')
	else:
		error = True
		errorTipo.append('Debe adjuntar los nombres como names')
	if(reqDict.__contains__('values')):
		try:
			valores = ast.literal_eval(reqDict.get('values'))
		except Exception:
			error=True
			errorTipo.append('values en formato incorrecto imposible Procesarlos')
		
		if(type(valores)!=list):
			error=True
			errorTipo.append('values en formato incorrecto utilize solo numeros')
	else:
		error = True
		errorTipo.append('Debe adjuntar los valores como values')
	if(len(nombres) == len(valores) and len(nombres)>0 and error is False):
		series = []
		if(tipoGraph=='line' or tipoGraph=='column' or tipoGraph=='bar'):
			for indx,item in enumerate(nombres):
				data =  OrderedDict({})
				data['name']=item
				if(type(valores[indx])==list):
					data['data']=valores[indx]
				else:
					data['data']=[valores[indx]]
				series.append(data)
			chart['series']=series
		elif(tipoGraph=='pie'):
			for indx,item in enumerate(nombres):
				try:
					float(valores[indx])
					series.append([item,valores[indx]])
				except Exception:
					error=True
					errorTipo.append('Valor '+str(indx+1)+' en formato incorrecto para pie')
					break
			chart['plotOptions']=OrderedDict({})
			chart['plotOptions']['pie']=OrderedDict({})
			chart['plotOptions']['pie']['allowPointSelect'] = True
			chart['plotOptions']['pie']['cursor'] = 'pointer'
			chart['series']=[]
			serie = OrderedDict({})
			serie['type']='pie'
			if not(chart['xAxis']['title']['text'] is None):
				serie['name']=chart['xAxis']['title']['text']
			elif not(chart['yAxis']['title']['text']):
				serie['name']=chart['yAxis']['title']['text']
			else:
				serie['name']=None
			serie['data']=series
			chart['series'].append(serie)
		else:
			error = True
			errorTipo.append('Tipo de grafico no soportado')
	else:
		error=True
		errorTipo.append('La cantidad de values y categorias no coinciden')
	if(error):
		errors['errors']=errorTipo
		return HttpResponse(simplejson.dumps(errors,use_decimal=True), mimetype='application/json')
	else:
		return HttpResponse(simplejson.dumps(chart,use_decimal=True), mimetype='application/json')