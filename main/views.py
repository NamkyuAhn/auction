from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Avg, Count, Q, Value, CharField, Func
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.models.functions import Concat

from .models import Item, Item_Image, Item_Entry
from .forms import ItemEntryForm

from datetime import datetime, date

class Round(Func):
    function = 'ROUND'
    template='%(function)s(%(expressions)s, 0)'
	
def main(request):
	return render(request, 'index.html', {})

def item_make(request):
	if request.user.is_authenticated:
		if request.method == 'POST':
			form = ItemEntryForm(request.POST)

			if form.is_valid():
				user_id = User.objects.get(id = request.user.id).id
				item = Item(
					name = form.data['item_name'],
					start_price = int(request.POST['price'].replace(",", "")),
					expire_date = request.POST['expire_date'],
					category_id = 1,
					is_expired = False,
					user_id = user_id,
				)
				item.save()
				
				item_image = Item_Image(
					item_id = item.id,
					image = request.FILES['image']
                )
				item_image.save()

				messages.info(request, "상품 정보가 등록되었습니다.")
				return redirect('main:main')

			else :
				messages.warning(request, "작성 폼을 올바르게 입력 하였는지 다시 한번 확인해 주세요.")
				return redirect('main:item_make')

		else: #GET일때
			form = ItemEntryForm()
			return render(request, 'item/item_make.html', {'form' : form})

	else: #로그인 안했을때
		messages.warning(request, "로그인 창으로 이동합니다.")
		return redirect('accounts:login')

def item_list(request):
    date_now = date(datetime.now().year, datetime.now().month, datetime.now().day)
    item_filter = Item.objects.filter(is_expired = False, expire_date__gte = date_now).prefetch_related("item_image")
    items = []
    for item in item_filter:
        image = Item_Image.objects.get(item_id = item.id)
        if Item_Entry.objects.filter(item_id = item.id).exists():
            entry = Item_Entry.objects.filter(item_id=item.id).order_by('-price')[0]
            items.append({
                 "id" : item.id,
                 "name" : item.name,
                 "start_price" : item.start_price,
                 "expire_date" : item.expire_date,
                 "highest_price" : entry.price,
                 "image" : image.image
            })
        else:
            items.append({
                 "id" : item.id,
                 "name" : item.name,
                 "start_price" : item.start_price,
                 "expire_date" : item.expire_date,
                 "highest_price" : 0,
                 "image" : image.image
                 })
    return render(request, 'item/item_list.html', {'items' : items})

def item_detail(request, item_id):
    item_filter = Item.objects.filter(id = item_id).prefetch_related("item_image")
    items = []
    for item in item_filter:
        image = Item_Image.objects.get(item_id = item.id)
        if Item_Entry.objects.filter(item_id = item.id).exists():
            entry = Item_Entry.objects.filter(item_id=item.id).order_by('-price')[0]
            items.append({
                 "id" : item.id,
                 "name" : item.name,
                 "start_price" : item.start_price,
                 "expire_date" : item.expire_date,
                 "highest_price" : entry.price,
                 "image" : image.image
            })
        else:
            items.append({
                 "id" : item.id,
                 "name" : item.name,
                 "start_price" : item.start_price,
                 "expire_date" : item.expire_date,
                 "highest_price" : 0,
                 "image" : image.image
                 })
    return render(request, 'item/item_detail.html', {'items' : items})

def item_entry(request):
    date_now = date(datetime.now().year, datetime.now().month, datetime.now().day)
    if request.user.is_authenticated:
        if request.method == 'POST':
            user_id = request.user.id
            item_id = request.POST['item_id']

            try:
                item = Item.objects.get(id=item_id)
                if item.user_id == user_id:
                    messages.warning(request, '본인 상품에는 입찰이 불가능합니다.')
                    return redirect(request.META.get('HTTP_REFERER', 'main:main'))
                
                elif item.expire_date < date_now:
                    messages.warning(request, '마감시한이 지나서 입찰이 불가능합니다.')
                    return redirect(request.META.get('HTTP_REFERER', 'main:main'))
                
                elif item.start_price >= int(request.POST['price'].replace(",", "")):
                    messages.warning(request, '최소 가격보다 높게 입찰해야 합니다.')
                    return redirect(request.META.get('HTTP_REFERER', 'main:main'))
                    
                elif Item_Entry.objects.filter(item_id = item_id):#다른사람 입찰 있을때
                    entry = Item_Entry.objects.filter(item_id=item.id).order_by('-price')[0]
                    if entry.price >= int(request.POST['price'].replace(",", "")):
                        messages.warning(request, '최고가보다 낮은 가격으로 입찰 할 수 없습니다')
                        return redirect(request.META.get('HTTP_REFERER', 'main:main'))
                    else:
                        if Item_Entry.objects.filter(user_id = user_id, item_id = item_id):
                            item = Item_Entry.objects.get(Q(user_id=user_id) & Q(item_id = item_id))

                            if item.price > int(request.POST['price'].replace(",", "")):
                                messages.warning(request, '낮은 가격으로 입찰 수정할 수 없습니다')
                                return redirect(request.META.get('HTTP_REFERER', 'main:main'))
                            Item_Entry.objects.filter(user_id = user_id, item_id = item_id).update(price=(request.POST['price'].replace(",", "")))
                            messages.success(request, '상품에 입찰하였습니다.')
                            return redirect('main:main')

                        else:
                            item_entry = Item_Entry(
                                user_id=user_id,
                                item_id=item_id,
                                price=int(request.POST['price'].replace(",", "")),
                                entered_date=date(datetime.now().year, datetime.now().month, datetime.now().day)
                            )
                            item_entry.save()
                            messages.success(request, '상품에 입찰하였습니다.')
                            return redirect('main:main')
                     
                elif Item_Entry.objects.filter(user_id = user_id, item_id = item_id):#다른사람 입찰x 사용자는 있을때
                    item = Item_Entry.objects.get(Q(user_id=user_id) & Q(item_id = item_id))

                    if item.price > int(request.POST['price'].replace(",", "")):
                        messages.warning(request, '낮은 가격으로 입찰 수정할 수 없습니다')
                        return redirect(request.META.get('HTTP_REFERER', 'main:main'))
                    Item_Entry.objects.filter(user_id = user_id, item_id = item_id).update(price=(request.POST['price'].replace(",", "")))
                    messages.success(request, '상품에 입찰하였습니다.')
                    return redirect('main:main')

                else:#사용자가 최초 입찰
                    item_entry = Item_Entry(
                        user_id=user_id,
                        item_id=item_id,
                        price=int(request.POST['price'].replace(",", "")),
                        entered_date=date(datetime.now().year, datetime.now().month, datetime.now().day)
                    )
                    item_entry.save()
                    messages.success(request, '상품에 입찰하였습니다.')
                return redirect('main:main')
                
            except Item.DoesNotExist:
                pass
    else:#비회원
        messages.warning(request, "로그인 창으로 이동합니다.")
        return redirect('accounts:login')
    
    return render(request, 'index.html')

def item_entry_list(request):
    items = Item_Entry.objects.filter(user_id = request.user.id)
    return render(request, 'item/item_entry_list.html', {'items' : items})

def item_mine_list(request):
    items = Item.objects.filter(user_id = request.user.id)
    return render(request, 'item/item_mine_list.html', {'items' : items})