import web_scraper as sc

path = "C:\\Users\\dinhd\\Downloads\\edgedriver_win64\\msedgedriver.exe"
df = sc.get_jobs('data scientist', 1000, False, path, 5)
print(df)
df.to_csv('glassdoor_jobs.csv', index = False)
