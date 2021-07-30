import pdfplumber
import csv
import os


def write_to_csv(data, mode='w'):
    keys = data.keys()
    with open ('pdf_data.csv', mode, newline='') as outfile:
        writer = csv.DictWriter(outfile, keys)
        if mode == 'w':
            writer.writeheader()
        writer.writerow(data)


filename = 'MayoTestCatalog-Rochester-LaboratoryReferenceEdition-SortedByTestName-duplex.pdf'
pdf = pdfplumber.open(filename)

keywords = ['Specimen Requirements:',
 'Specimen Minimum Volume:',
 'Transport Temperature:',
 'SpecimenType',
 'Temperature',
 'Time',
 'SpecialContainer',
 'CPT Code Information:']

all_text_list = []
all_tables = []
for i in range(11, 50):
    page = pdf.pages[i]
    text = page.extract_text()
    text_list = text.split('\n')
    text_list = text_list[:-1]
    all_text_list.extend(text_list)
    page_tables = page.extract_tables()
    all_tables.extend(page_tables)
    # print(len(all_tables))

counter = 0
for line in all_text_list:
    if keywords[-1] in line:
        sub_text_list = all_text_list[:all_text_list.index(line)+1]
        # print(sub_text_list)
        all_text_list = all_text_list[all_text_list.index(line)+1 : ]
    else:
        continue

    table = all_tables[counter]
    counter += 1
    data = {}
    text = ' '.join(sub_text_list)
    code = sub_text_list[0].split()[0]
    number = sub_text_list[1].split()[0]
    other_name = ' '.join(sub_text_list[0].split()[1:])

    spec_requirements = text.partition(keywords[0])[2].partition(keywords[1])[0]
    spec_requirements = ' '.join(spec_requirements.split('\n'))

    spec_min_volume = text.partition(keywords[1])[2].partition(keywords[2])[0]
    spec_min_volume = ' '.join(spec_min_volume.split('\n'))

    table_dict = {key:' ' for key in table[0]}
    keys = list(table_dict.keys())
    for row in table[1:]:
        for i in range(len(keys)):
            if not row[i]:
                row[i] = ''
            table_dict[keys[i]] += ' '+row[i]

    for line in sub_text_list:
        if keywords[-1] in line:
            cpt_code = line.split(':')[-1]
            break

    data['code'] = code
    data['number'] = number
    data['other name'] = other_name
    data['specimen requirements'] = spec_requirements
    data['specimen min value'] = spec_min_volume
    data.update(table_dict)
    data['cpt code information'] = cpt_code
    print(data)
    print()
    if os.path.exists('pdf_data.csv'):
        write_to_csv(data, mode='a')
    else:
        write_to_csv(data, mode='w')
