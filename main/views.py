from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Avg, Count, Q, Value, CharField, Func
from django.db.models.functions import Concat

class Round(Func):
    function = 'ROUND'
    template='%(function)s(%(expressions)s, 0)'
	
def main(request):
	return render(request, 'index.html', {})

