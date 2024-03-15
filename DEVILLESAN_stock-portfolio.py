#ALDRICH NATHANIEL L. DEVILLES
#T7L
#Stock Portfolio Tracking System with Save and Load


def load_portfolio(stocks):
    fileHandle = open("portfolio.txt", "r")
    for stockData in fileHandle:
        data = stockData[:-1].split(",")
        if data[0] == "CASH":
            cashSymbol = data[0]
            cashDesc = "Cash"
            cashQuantity = data[1]
            cashPrice = 1
            cashComputedTotal = cashQuantity * cashPrice
            stocks[cashSymbol] = [cashDesc, float(cashQuantity), int(cashPrice), float(cashComputedTotal)]
        else:
            stockSymbol = data[0]
            stockDesc = data[1]
            stockQuantity = data[2]
            stockPrice = data[3]
            stockComputedTotal = float(stockQuantity) * float(stockPrice)
            stocks[stockSymbol] = [stockDesc, int(stockQuantity), float(stockPrice), float(stockComputedTotal)]
    fileHandle.close()

def save_portfolio(stocks):
    
    fileHandle = open("portfolio.txt", "w")
    for stockkey, stockvalue in stocks.items():
        if stockkey == "CASH":
            fileHandle.write(f"{stockkey},{stockvalue[1]}\n")
        else:
            stock_symbol = stockkey
            stock_desc = stockvalue[0]
            stock_quantity = stockvalue[1]
            stock_price = stockvalue[2]
            fileHandle.write(f"{stock_symbol},{stock_desc},{stock_quantity},{stock_price}\n")
    fileHandle.close()


#This functions lets the user view their stock portfolio
def viewPortfolio(stocks):
    print("PORTFOLIO")
    print("---------")
    #By using the \t command, it makes the program's interface better as the
    print("\nSymbol \t\t Description \t\t\t\t Quantity \t\t Price \t\t\t Value")
    print("------ \t\t ------------------- \t\t -------- \t\t --------- \t\t ---------")
    #This is the summation of all the values of each stock(stockQuantity*stockPrice)
    totalValue = 0
    #This formats the data into a currency format if needed
    for stock, stock_info in stocks.items():
        #Each value of a key is a list with 4 data (0= stockDesc, 1=stockQuantity, 2=stockPrice, 3=stockValue)
        for info in range(0, 4):
            #Formats stockPrice
            if info == 2:
                stockPriceFormatted = "{:.2f}".format(stock_info[2])
            #Formats stockValue
            if info == 3:
                #since it is a stock value, let us add it to total value
                totalValue += float(stock_info[3])
                stockValueFormatted = "{:.2f}".format(float(stock_info[3]))
        #This prints the information in a formatted way
        print(f"{format(stock, '<12')} {format(stock_info[0], '<12')} {format(stock_info[1], '>23')} {format(stockPriceFormatted, '>16')} {format(stockValueFormatted, '>15')}")
    #This prints the total value in a formatted way
    totalValueFormatted = "{:.2f}".format(totalValue)
    print(f"\n{format('TOTAl', '>66')} {format(totalValueFormatted, '>15')}")

#This functions lets the user buy a stock
def buyStock(stocks):
    #We will subtract the stocks bought from cash balance
    cashBalance = float(stocks["CASH"][3])
    print("BUY STOCK")
    print("---------")
    stockSymbol = input("Enter symbol: ").upper()

    #If the entered symbol does not exist in our dictionary, we let them enter the information of the new stock
    if stockSymbol not in stocks:
        print("\nINFO: Initial entry of ", stockSymbol, "\n")
        stockDesc = input("Enter Company Name: ")
        stockQuantity = int(input("Enter # of shares to buy: "))
        stockPrice = float(input("Enter current price per share: "))
        computedTotal = stockQuantity * stockPrice
        #This checks if the the stocks that will be bought, is less than the cash balance because you won't be able to buy something greater than your balance
        if computedTotal < cashBalance:
            print("\nINFO:", stockQuantity, "shares of", stockSymbol, "purchased for a total of", computedTotal)
            #STOCK DICTIONARY UPDATE
            stocks[stockSymbol] = [stockDesc, stockQuantity, stockPrice, computedTotal]
            stocks["CASH"][1] -= computedTotal
            stocks["CASH"][3] -= computedTotal
        #Prints this if cash is insufficient
        else:
            print("\nERROR: Not enough Cash")

    #If the entered symbol exist in our dictionary, we let them buy immediately with the same process above
    else:
        print("\nINFO: Adding more shares of", stockSymbol,"\n")
        stockQuantity = int(input("Enter # of shares to buy: "))
        newStockQuantity = stockQuantity + stocks[stockSymbol][1]
        stockPrice = float(input("Enter current price per share: "))
        boughtTotal = stockQuantity * stockPrice
        computedTotal = newStockQuantity * stockPrice
        if computedTotal < cashBalance:
            print("\nINFO:", stockQuantity, "shares of", stockSymbol, "purchased for a total of", boughtTotal)
            # STOCK DICTIONARY UPDATE
            stocks["CASH"][1] -= boughtTotal
            stocks["CASH"][3] -= boughtTotal
            stocks[stockSymbol][1] += stockQuantity
            stocks[stockSymbol][2] = stockPrice
            stocks[stockSymbol][3] = computedTotal

        else:
            print("\nERROR: Not enough Cash")
        ####

#This functions lets the user sell their stock
def sellStock(stocks):
    cashBalance = float(stocks["CASH"][3])
    print("SELL STOCK")
    print("---------")
    #We can't sell the CASH in our dictionary
    # If the length of our dictionary is one, it means that we only have CASH in our portfolio and we don't have any stocks
    # The length of our stocks dictionary is always greater than or equal to 1.
    if len(stocks) != 1:
        stockSymbol = input("Enter symbol: ").upper()
        #This checks if the inputted symbol is in the stocks
        if stockSymbol in stocks:
            assetBalance = float(stocks[stockSymbol][1])
            #This checks if the stock inputted has a remaining balance in terms of stockQuantity
            if assetBalance != 0:
                stockQuantity = int(input("Enter # of shares to sell: "))
                #This checks if the user wants to sell stock less than their balance since we can't sell stock beyond what we currently have
                if assetBalance >= stockQuantity:
                    stockPrice = float(input("Enter current price per share: "))
                    converted_Value = stocks[stockSymbol][1] * stockPrice
                    computedTotal = stockQuantity * stockPrice
                    # If user wants to sell all his stock, the stock is deleted form the stocks dictionary
                    if assetBalance-stockQuantity == 0:
                        del stocks[stockSymbol]
                    #STOCK DICTIONARY UPDATE
                    else:
                        stocks[stockSymbol][1] -= stockQuantity
                        stocks[stockSymbol][2] = stockPrice
                        stocks[stockSymbol][3] = converted_Value - computedTotal
                    stocks["CASH"][1] += computedTotal
                    stocks["CASH"][3] += computedTotal

                    print("INFO: Sold", stockQuantity, "shares of", stockSymbol, "for total of","{:.2f}".format(computedTotal))
                else:
                    print("\nERROR: Not enough shares")
            else:

                print("\nERROR: No stock assets to sell")
        else:
            print("\nERROR:", stockSymbol, "not in portfolio")
    else:
        print("\nERROR: No stock assets to sell")

    
#This functions lets the user change the value of a stock
def changePrice(stocks):
    print("CHANGE PRICE")
    print("------------")
    # We can't change the value of CASH in our dictionary
    # If the length of our dictionary is one, it means that we only have CASH in our portfolio and we don't have any stocks to change pricce
    # The length of our stocks dictionary is always greater than or equal to 1.
    if len(stocks) != 1:
        stockSymbol = input("Enter symbol: ").upper()
        #This checks if the stock symbol we inputted exists in our portfolio
        if stockSymbol in stocks:
            stockQuantity = stocks[stockSymbol][1]
            #This checks if our stock has shares.
            if stockQuantity != 0:
                #This allows the user to change the stock price
                currentPrice = float(input("Enter current price per share: "))
                stocks[stockSymbol][3] = currentPrice * stockQuantity
                stocks[stockSymbol][2] = currentPrice
            else:
                print("\nERROR:", stockSymbol, "has no shares")
        else:
            print("\nERROR:", stockSymbol, "not in portfolio")
    else:
        print("\nERROR: No stock assets to change")



#This function lets the user liquidate all of their stocks
def sellAll(stocks):
    print("LIQUIDATE ALL STOCKS")
    print("--------------------")
    # We can't sell our CASH in our dictionary
    # If the length of our dictionary is one, it means that we only have CASH in our portfolio and we don't have any stocks to sell
    # The length of our stocks dictionary is always greater than or equal to 1.
    if len(stocks) != 1:
        sellAllStocks = input("Are you sure you want to sell all your stocks? [Y to confirm]: ").upper()
        #Checks if the user really wants to sell all their stocks
        if sellAllStocks == "Y":
            print()
            for stock in stocks:
                # We can't sell our CASH in our dictionary
                if stock != "CASH":
                    stockQuantity = stocks[stock][1]
                    stockPrice = stocks[stock][2]
                    computedTotal = stockQuantity * stockPrice
                    # STOCK DICTIONARY UPDATE
                    stocks[stock][1] -= stockQuantity
                    stocks[stock][2] = 0
                    stocks[stock][3] -= computedTotal
                    stocks["CASH"][1] += computedTotal
                    stocks["CASH"][3] += computedTotal
                    print("INFO: Sold",stockQuantity,"shares of", stock, "for total of", "{:.2f}".format(computedTotal))
            #This deletes the stock after the program sells all the stock
            #This grabs all the keys in the dictionary and converts it into a list
            for index in list(stocks.keys()):
                #This checks if the index 0 is not Cash
                #If it is not Cash, it deletes the stock
                if stocks[index][0] != "Cash":
                    del stocks[index]

        else:
            print("\nERROR: No Action Done")
    else:
        print("\nERROR: No stock assets to liquidate")


#This function is the menu function
def menu():
    print("========== MENU ==========")
    print("[1] View Portfolio")
    print("[2] Buy Stock")
    print("[3] Sell Stock")
    print("[4] Change Stock Price")
    print("[5] Liquidate All Stocks")
    print("[6] Exit")
    print("==========================")





#================ MAIN PROGRAM =====================


endProgram = False
#This is the initial value of our stocks dictionary
#It will be edited as the user use the program
stocks = {"CASH":
          ["Cash", 10000, 1, 10000],
}

load_portfolio(stocks)
#The program repeats until endProgram is False
while not endProgram:
    menu()
    choice = int(input("Enter option: "))
    print()

    #View portfolio
    if choice == 1:
        viewPortfolio(stocks)
        save_portfolio(stocks)
    #Buy stocks
    elif choice == 2:
        buyStock(stocks)
        save_portfolio(stocks)
    #Sell stocks
    elif choice == 3:
        sellStock(stocks)
        save_portfolio(stocks)
    #Change price
    elif choice == 4:
        changePrice(stocks)
        save_portfolio(stocks)
    #Sell all stocks
    elif choice == 5:
        sellAll(stocks)
        save_portfolio(stocks)
    #Exits the program
    elif choice == 6:
        print("Goodbye!")
        endProgram = True
    #Execute this is if input is not in menu choices
    #This does not end the program and will just loop it back to menu
    else:
        print("ERROR: Invalid Option")

