
#!/usr/bin/env python
# -*- coding: utf-8 -*-

analyze_code = []
billing_code = []
test_name = []
sample_type = []
handled_descriptions = ['']

test_file = open("input_files/testName.txt")
sample_file = open("input_files/sampleType.txt")
analyze_file = open("input_files/analyzeCode.txt")
billing_file = open("input_files/billingCode.txt")
result = open("output_files/testCodeResult.sql",'w')

def esc_char(name):
    if "'" in name:
        return "$$" + name + "$$"
    else:
        return "'" + name + "'"

def remove_test_name_markup( test_name):
    if '*' in test_name:
        test_name = test_name.split(')')[1].strip()

    return test_name

def create_description( test_name, sample_type):
    test_name = remove_test_name_markup(test_name)

    if ',' in sample_type:
        sample_type = ''
    else:
        sample_type =  '(' + sample_type + ')'

    return esc_char(test_name + sample_type )


for line in test_file:
    test_name.append(line.strip())
test_file.close()

for line in sample_file:
    sample_type.append(line.strip())
sample_file.close()

for line in analyze_file:
    analyze_code.append(line.strip())
analyze_file.close()

for line in billing_file:
    billing_code.append(line.strip())
billing_file.close()

write_analyze_code = len(analyze_code) > 0
write_billing_code = len(billing_code) > 0

if not( write_analyze_code or write_billing_code ):
    print 'No test code entries'
    exit()

for row in range(0, len(test_name)):
    if len(test_name[row]) > 1:
        description = create_description(test_name[row], sample_type[row] )
        if description.strip() not in handled_descriptions:
                handled_descriptions.append( description.strip())
                if write_billing_code:
                    result.write("INSERT INTO test_code( test_id, code_type_id, value, lastupdated) \n\t")
                    result.write("VALUES ( (select id from clinlims.test where description = " + description + " ), " )
                    result.write( "(select id from clinlims.test_code_type where schema_name = 'billingCode'), '"+  billing_code[row] + "', now() );\n")

                if write_analyze_code:
                    result.write("INSERT INTO test_code( test_id, code_type_id, value, lastupdated) \n\t")
                    result.write("VALUES ( (select id from clinlims.test where description = " + description + " ), " )
                    result.write( "(select id from clinlims.test_code_type where schema_name = 'analyzeCode'), '" +  analyze_code[row] + "', now() );\n")

result.close()

print "Done check testCodeResult.sql for values"



#    VALUES ( (select id from clinlims.test where description = 'Test de VIH' ), (select id from clinlims.test_code_type where schema_name = 'billingCode'), 'B120', now() );

