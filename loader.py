import sys

companies = []
for line in open(sys.argv[1]):
    companies.append(eval(line.strip()))

print(companies)