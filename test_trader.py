from Classes import trader



def makeOrder(currentPrice, trader):
    if(currentPrice > .2*trader.bank):
        order = 1
    else:
        order = -1
    return order

    