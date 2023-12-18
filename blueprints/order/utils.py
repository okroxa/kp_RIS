from flask import session

def clear_order():
    if 'order' in session:
        session.pop('order')

def add_to_basket(item):
    basket=session.get('order',[])
    id = int(item[0]['idMenu'])

    bask=item[0]
    i=0
    for b in basket:
        if b['idMenu']==id:
            basket[i]['number']+=1
            session['order'] = basket
            return
        i+=1

    num={'number':1}
    bask.update(num)
    basket.append(bask)
    session['order']=basket


def change(id):
    id=int(id)
    i = 0
    basket=session.get('order',[])
    for b in basket:
        if b['idMenu']==id:
            if b['number']==1:
                basket.remove(b)
                session['order']=basket
                return
            else:
                basket[i]['number'] -= 1
                session['order'] = basket
                return
        i+=1