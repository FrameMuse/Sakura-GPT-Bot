import csv
import time

filename = 'example.csv'
data = []

with open(filename, 'r', encoding='cp1251') as file:
    reader = csv.reader(file)
    for row in reader:
        data.append(','.join(row))

print(data)

base_str = '<?xml version="1.0" encoding="utf-8"?>\n<RegistrySet xsi:noNamespaceSchemaLocation="schema.xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'

for person in data:

    values = person.split(';')

    # Создаем словарь для хранения данных
    data = {
        'lastName': values[0],
        'firstName': values[1],
        'middleName': values[2],
        'snils': values[3],
        'employerTitle': values[4],
        'employerInn': values[5],
        'position': values[6],
        'organizationTitle': values[7],
        'organizationInn': values[8],
        'protocolNumber': values[9],
        'learnProgramTitle': values[10],
        'testDate': values[11],
        'testStatus': values[12],
        'testPassDate': values[13]
    }

    if data['lastName'] == "Фамилия":
        continue

    base_str += f'\n  <RegistryRecord>\n    <Worker>\n      <LastName>{data["lastName"]}</LastName>\n      <FirstName>{data["firstName"]}</FirstName>\n      <MiddleName>{data["middleName"]}</MiddleName>\n      <Snils>{data["snils"]}</Snils>\n      <Position>{data["position"]}</Position>\n      <EmployerInn>{data["employerInn"]}</EmployerInn>\n      <EmployerTitle>{data["employerTitle"]}</EmployerTitle>\n    </Worker>\n    <Organization>\n      <Inn>{data["organizationInn"]}</Inn>\n      <Title>{data["organizationTitle"]}</Title>\n    </Organization>\n    <Test isPassed="{data["testStatus"].lower() == "пройден"}" learnProgramId="1">\n      <Date>{data["testDate"]}</Date>\n      <ProtocolNumber>{data["protocolNumber"]}</ProtocolNumber>\n      <LearnProgramTitle>{data["learnProgramTitle"]}</LearnProgramTitle>\n    </Test>\n  </RegistryRecord>'



base_str+="\n</RegistrySet>"
print(base_str)


with open(str(time.time()) + '-file.xml', 'w') as f:
    f.write(base_str)
