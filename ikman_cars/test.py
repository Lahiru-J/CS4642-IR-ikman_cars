with open('urls.csv', 'w') as f:
    for i in range(1,401):
        f.write('https://ikman.lk/en/ads/sri-lanka/cars-vehicles?categoryType=ads&categoryName=Cars+%26+Vehicles&page='+str(i)+'\n')
