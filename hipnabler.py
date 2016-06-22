import imp, os.path as path

print()
print("Beginning Results Formatting.")
#Filename refactoring.
lotus = path.realpath('.')
#Import the skeleton module.
cxie = imp.load_source('cxie', path.join(lotus, 'test_project.py'))
#Get the Unique Names
meteor = list(dict(cxie.TestUnification.__dict__).keys())
#Filter to the Identified.
meteor = list(filter(lambda x: '_uid' in x and 'test_' in x, meteor))
#Read out the Verdict
st = open(path.join(lotus, 'REGR.tap'), 'rt')
strahl = ''.join(st.readlines())
st.close()
#Apply the Name Alteration.
for x in meteor:
    strahl = strahl.replace(x.split('_uid')[0], x)
#Write out the results.
pap = open(path.join(lotus, 'REGR.tap'), 'wt')
pap.write(strahl)
pap.close()
print("Results Formatted.")
print()
