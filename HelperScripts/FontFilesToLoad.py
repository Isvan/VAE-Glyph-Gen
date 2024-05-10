import glob
txtfiles = []
for file in glob.glob("*.ttf"):
    txtfiles.append(file)

for file in glob.glob("*.otf"):
    txtfiles.append(file)

print(txtfiles)


