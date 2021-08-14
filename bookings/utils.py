def reArrangeOrder(orderStr, id):
    # print("orderStr before: ", orderStr)
    orderList = []
    orderList = orderStr.split(',')
    newOrderList = []

    for order in orderList:
        if(order != str(id)):
            newOrderList.append(order)
    # print("new List: ", newOrderList)
    if (newOrderList == '') or (newOrderList is None):
        return newOrderList

    newOrderStr = ",".join(newOrderList)
    # print('order str after: ', newOrderStr)
    return newOrderStr
