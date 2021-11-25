import numpy as np

def AveragePrice(prices):
    return np.mean(prices) 

def RangePrice(prices):
    return np.ptp(prices) 

def quartileprice(numbers):
    length = len(numbers) 
    numbers.sort()
    index1 = int((length+1)/4)-1 
    index2= int((length+1)/2)-1 
    index3 = int(3*(length+1)/4)-1
    q1 = numbers[index1] 
    q2 = numbers[index2] 
    q3= numbers[index3]
    return q1, q2, q3

def StdPrices(prices):
    return np.std(prices)

def cov(prices):
    return np.std(prices)/np.mean(prices)


def main():
    numbers = [1, 2, 3, 4, 5]
    print(AveragePrice(numbers))
    print(RangePrice(numbers))
    print(StdPrices(numbers))
    print(cov(numbers))
    print("quartile of the stock prices are", quartileprice(numbers))
    
    
if __name__ == "__main__":
    main()


